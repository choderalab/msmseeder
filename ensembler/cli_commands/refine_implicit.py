import ensembler
import ensembler.refinement
import simtk.unit as unit

helpstring_header = """\
Refine models by molecular dynamics simulation with implicit solvent (generalized Born surface
area), using OpenMM.

Each MD simulation is preceded by a steepest-descent energy minimzation.

The final refined structure is written as "implicit-refined.pdb.gz" in the model directory.

MPI-enabled.

Options:"""

helpstring_unique_options = [
    """\
  --openmm_platform <platform>    Specify the OpenMM Platform to use {CUDA|OpenCL|CPU|Reference}
                                  (default is to auto-select the fastest platform availble).""",

    """\
  --gpupn <gpupn>                 If using GPUs, specify how many are available per node
                                  [default: 1].""",

    """\
  --simlength <simlength>         Simulation length (ps) [default: 100.0].""",

    """\
  --retry_failed_runs             Retry simulation runs which previously failed, e.g. due to bad
                                  inter-atom contacts.""",
]

helpstring_nonunique_options = [
    """\
  --targetsfile <targetsfile>  File containing a list of target IDs to work on (newline-separated).
                               Comment targets out with "#".""",

    """\
  --targets <target>           Define one or more target IDs to work on (comma-separated), e.g.
                               "--targets ABL1_HUMAN_D0,SRC_HUMAN_D0" (default: all targets)""",

    """\
  --templates <template>       Define one or more template IDs to work on (comma-separated), e.g.
                               "--templates ABL1_HUMAN_D0_1OPL_A" (default: all templates)""",

    """\
  -v --verbose                 """,
]

helpstring = '\n\n'.join([helpstring_header, '\n\n'.join(helpstring_unique_options), '\n\n'.join(helpstring_nonunique_options)])
docopt_helpstring = '\n\n'.join(helpstring_unique_options)

def dispatch(args):
    if args['--targetsfile']:
        with open(args['--targetsfile'], 'r') as targetsfile:
            targets = [line.strip() for line in targetsfile.readlines() if line[0] != '#']
    elif args['--targets']:
        targets = args['--targets'].split(',')
    else:
        targets = False

    if args['--templates']:
        templates = args['--templates'].split(',')
    else:
        templates = False

    if args['--gpupn']:
        gpupn = int(args['--gpupn'])
    else:
        gpupn = 1

    if args['--simlength']:
        sim_length = float(args['--simlength']) * unit.picoseconds
    else:
        sim_length = 100.0 * unit.picoseconds

    if args['--verbose']:
        loglevel = 'debug'
    else:
        loglevel = 'info'

    ensembler.refinement.refine_implicit_md(openmm_platform=args['--openmm_platform'], gpupn=gpupn, sim_length=sim_length, process_only_these_targets=targets, process_only_these_templates=templates, retry_failed_runs=args['--retry_failed_runs'], verbose=args['--verbose'])