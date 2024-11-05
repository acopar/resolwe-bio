"""Gene fusion detection with Arriba."""

import re
from pathlib import Path

import pandas as pd
from plumbum import TEE

from resolwe.process import Cmd, DataField, FileField, Process, SchedulingClass


def get_contig_names(gtf_file):
    """Get sorted unique contig names.

    List of contig (chromosome) names is required by arriba (parameter -i).
    This function covers possible edge cases where contig names are not common.
    """

    gtf = pd.read_csv(
        gtf_file, sep="\t", header=None, usecols=[0], dtype={0: str}, comment="#"
    )

    contigs = sorted(set(gtf[0]))
    out = " ".join(contigs)
    return out


class Arriba(Process):
    """Run Arriba for fusion detection from RNA-Seq data.

    This process detects gene fusions from RNA-Seq data using the Arriba tool.
    The input can be a BAM file from the STAR aligner, and additional optional
    inputs such as blacklist, protein domains, and known fusions files can be provided.
    More information about Arriba can be found in the
    [Arriba manual](https://arriba.readthedocs.io/en/latest/) and in
    the [original paper](https://genome.cshlp.org/content/31/3/448)
    The current version of Arriba is 2.4.0.
    """

    slug = "arriba"
    name = "Arriba"
    process_type = "data:genefusions:arriba"
    version = "1.1.1"
    category = "Gene fusions"
    scheduling_class = SchedulingClass.BATCH
    entity = {"type": "sample"}
    requirements = {
        "expression-engine": "jinja",
        "executor": {
            "docker": {"image": "public.ecr.aws/genialis/resolwebio/rnaseq:6.3.0"}
        },
        "resources": {
            "cores": 1,
            "memory": 16384,
        },
    }
    data_name = '{{ bam|name|default("?") }}'

    class Input:
        """Input fields for Arriba process."""

        bam = DataField(
            data_type="alignment:bam",
            label="Input BAM file from STAR ran with parameters suggested by Arriba",
        )

        gtf = DataField(
            data_type="annotation:gtf",
            label="GTF file",
            description="Annotation file in GTF format.",
        )

        genome = DataField(
            data_type="seq:nucleotide",
            label="Genome file",
            description="Genome file in FASTA format.",
        )

        blacklist_file = DataField(
            data_type="file",
            label="Blacklist file",
            description="Arriba blacklist file.",
            required=False,
        )

        known_fusions_file = DataField(
            data_type="file",
            label="Known fusions file",
            description="Arriba known fusions file.",
            required=False,
        )

    class Output:
        """Output fields for Arriba process."""

        fusions = FileField(label="Predicted fusions")
        discarded_fusions = FileField(label="Discarded fusions")

    def run(self, inputs, outputs):
        """Run Arriba to detect fusions from RNA-Seq data."""

        bam_file = inputs.bam.output.bam.path
        bam_fn = Path(bam_file).name

        output_file = f"{bam_fn}_fusions.tsv"
        discarded_fusions_file = f"{bam_fn}_discarded_fusions.tsv"

        return_code, stdout, stderr = Cmd["samtools"]["head", bam_file] & TEE(
            retcode=None
        )

        if return_code:
            print(stdout, stderr)
            self.error("Samtools head command failed. Check BAM file integrity.")

        if not "ID:STAR" in stdout:
            self.error(
                "The input BAM file was not generated by STAR aligner. "
                "Please provide a BAM file generated by STAR."
            )

        co_line = next(
            (line for line in stdout.splitlines() if line.startswith("@CO")), None
        )

        if co_line:
            segment_match = re.search(r"--chimSegmentMin (\d+)", co_line)
            if not segment_match or not int(segment_match.group(1)) > 0:
                self.error(
                    "STAR parameters were not set correctly. "
                    "Please check that the --chimSegmentMin parameter was passed when aligning using STAR and was not zero."
                )
        else:
            self.error("STAR parameters cannot be inferred from header.")

        contigs = get_contig_names(gtf_file=inputs.gtf.output.annot.path)

        args = [
            "-x",
            bam_file,
            "-o",
            output_file,
            "-O",
            discarded_fusions_file,
            "-g",
            inputs.gtf.output.annot.path,
            "-a",
            inputs.genome.output.fasta.path,
            "-i",
            contigs,
        ]

        if inputs.blacklist_file:
            args.extend(["-b", inputs.blacklist_file.output.file.path])
        else:
            args.extend(["-f", "blacklist"])

        if inputs.known_fusions_file:
            args.extend(["-k", inputs.known_fusions_file.output.file.path])

        return_code, stdout, stderr = Cmd["arriba"][args] & TEE(retcode=None)

        if return_code:
            print(stdout, stderr)
            self.error("Arriba process failed.")

        Cmd["gzip"][output_file]()
        Cmd["gzip"][discarded_fusions_file]()

        outputs.fusions = f"{output_file}.gz"
        outputs.discarded_fusions = f"{discarded_fusions_file}.gz"
