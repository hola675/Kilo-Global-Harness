"""Carga el parser canónico desde tools/ bajo unittest -I."""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARSER = ROOT / "tools" / "dev_team_agent_parser.py"
spec = spec_from_file_location("vx_dev_team_agent_parser", PARSER)
if spec is None or spec.loader is None:
    raise ImportError(f"No se pudo cargar {PARSER}")
module = module_from_spec(spec)
spec.loader.exec_module(module)

AgentDocument = module.AgentDocument
AgentPermissions = module.AgentPermissions
extract_frontmatter = module.extract_frontmatter
parse_permission_block = module.parse_permission_block
load_agent = module.load_agent
get_skill_allowlist = module.get_skill_allowlist
get_task_allowlist = module.get_task_allowlist
iter_agents = module.iter_agents
