#!/usr/bin/env python3
"""
Claude Code Automation Framework - Project Wizard
Interactive tool to create new projects with appropriate templates and tech stacks.
"""

import os
import sys
import shutil
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class ProjectWizard:
    """Interactive project creation wizard."""
    
    def __init__(self, args=None):
        """Initialize the project wizard."""
        self.framework_path = Path(__file__).parent.parent
        self.templates_path = self.framework_path / "templates" / "application_types"
        self.tech_stacks_path = self.framework_path / "tech_stacks"
        self.args = args
        
    def run(self) -> None:
        """Run the interactive project wizard."""
        print("🚀 Claude Code Automation Framework - Project Wizard")
        print("=" * 50)
        
        # Get project details
        project_name = self._get_project_name()
        app_type = self._select_application_type()
        tech_stack = self._select_tech_stack(app_type)
        project_path = self._get_project_path(project_name)
        
        # Create project
        self._create_project_structure(project_path)
        self._generate_prd(project_path, project_name, app_type)
        self._setup_tech_stack(project_path, tech_stack)
        self._create_framework_link(project_path)
        
        print(f"\n✅ Project '{project_name}' created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"\n🎯 Next steps:")
        print(f"1. cd {project_path}")
        print(f"2. Complete the PRD.md file with your specific requirements")
        print(f"3. Run: python -c 'import sys; sys.path.append(\"{self.framework_path}\"); from core.development_guide import start_development'")
        
    def _get_project_name(self) -> str:
        """Get project name from user or args."""
        if self.args and self.args.name:
            name = self.args.name
            if name and name.replace("_", "").replace("-", "").isalnum():
                return name
            print(f"❌ Invalid project name: {name}")
            sys.exit(1)
        
        while True:
            try:
                name = input("\n📝 Enter project name: ").strip()
                if name and name.replace("_", "").replace("-", "").isalnum():
                    return name
                print("❌ Please enter a valid project name (letters, numbers, hyphens, underscores)")
            except EOFError:
                print("\n❌ Error: No input available. Please run this wizard in an interactive terminal.")
                print("💡 Use command line arguments: python tools/project_wizard.py --name PROJECT_NAME --type TYPE")
                sys.exit(1)
    
    def _select_application_type(self) -> str:
        """Let user select application type."""
        app_types = {
            "1": ("web_app", "Web Application (React/Vue + Backend)"),
            "2": ("cli_tool", "Command Line Tool"),
            "3": ("api_service", "REST API / Microservice"),
            "4": ("ml_system", "Machine Learning System"),
            "5": ("trading_dashboard", "Trading/Financial Dashboard"),
        }
        
        type_mapping = {
            "web_app": "1",
            "cli_tool": "2", 
            "api_service": "3",
            "ml_system": "4",
            "trading_dashboard": "5"
        }
        
        if self.args and self.args.type:
            app_type = self.args.type
            if app_type in type_mapping:
                return app_type
            elif app_type in app_types:
                return app_types[app_type][0]
            else:
                print(f"❌ Invalid application type: {app_type}")
                print("Valid types: web_app, cli_tool, api_service, ml_system, trading_dashboard")
                sys.exit(1)
        
        print("\n🎯 Select application type:")
        for key, (_, description) in app_types.items():
            print(f"  {key}. {description}")
        
        while True:
            try:
                choice = input("\nEnter choice (1-5): ").strip()
                if choice in app_types:
                    return app_types[choice][0]
                print("❌ Please enter a number between 1-5")
            except EOFError:
                print("\n❌ Error: No input available. Please run this wizard in an interactive terminal.")
                print("💡 Use command line arguments: python tools/project_wizard.py --name PROJECT_NAME --type TYPE")
                sys.exit(1)
    
    def _select_tech_stack(self, app_type: str) -> Optional[Dict]:
        """Let user select technology stack."""
        available_stacks = self._get_available_tech_stacks(app_type)
        
        if not available_stacks:
            print(f"\n⚠️  No pre-configured tech stacks found for {app_type}")
            return None
        
        # If using command line args, use first available stack
        if self.args and (self.args.name or self.args.type):
            filename = list(available_stacks.keys())[0]
            selected_stack = available_stacks[filename]
            print(f"\n⚙️  Using default tech stack: {selected_stack['name']}")
            return selected_stack
        
        print(f"\n⚙️  Available tech stacks for {app_type}:")
        for i, (filename, stack_info) in enumerate(available_stacks.items(), 1):
            print(f"  {i}. {stack_info['name']} - {stack_info['description']}")
        
        while True:
            try:
                choice = int(input(f"\nSelect tech stack (1-{len(available_stacks)}): "))
                if 1 <= choice <= len(available_stacks):
                    filename = list(available_stacks.keys())[choice - 1]
                    return available_stacks[filename]
                print(f"❌ Please enter a number between 1-{len(available_stacks)}")
            except ValueError:
                print("❌ Please enter a valid number")
            except EOFError:
                print("\n❌ Error: No input available. Please run this wizard in an interactive terminal.")
                print("💡 Use command line arguments: python tools/project_wizard.py --name PROJECT_NAME --type TYPE")
                sys.exit(1)
    
    def _get_available_tech_stacks(self, app_type: str) -> Dict[str, Dict]:
        """Get available tech stacks for the application type."""
        stacks = {}
        
        for stack_file in self.tech_stacks_path.glob("*.yaml"):
            try:
                with open(stack_file, 'r') as f:
                    stack_info = yaml.safe_load(f)
                    
                if app_type in stack_info.get('application_types', []):
                    stacks[stack_file.name] = stack_info
                    
            except Exception as e:
                print(f"⚠️  Error loading {stack_file}: {e}")
        
        return stacks
    
    def _get_project_path(self, project_name: str) -> Path:
        """Get project path from user or use default."""
        default_path = Path.cwd() / project_name
        
        # If using command line args, use default path
        if self.args and (self.args.name or self.args.type):
            print(f"\n📁 Using default project location: {default_path}")
            return default_path
        
        try:
            path_input = input(f"\n📁 Project location [{default_path}]: ").strip()
            if not path_input:
                return default_path
            
            return Path(path_input).expanduser().resolve()
        except EOFError:
            print("\n❌ Error: No input available. Please run this wizard in an interactive terminal.")
            print("💡 Use command line arguments: python tools/project_wizard.py --name PROJECT_NAME --type TYPE")
            sys.exit(1)
    
    def _create_project_structure(self, project_path: Path) -> None:
        """Create the basic project directory structure."""
        if project_path.exists():
            # If using command line args, auto-continue if directory exists
            if self.args and (self.args.name or self.args.type):
                print(f"\n⚠️  Directory {project_path} already exists. Continuing...")
            else:
                try:
                    response = input(f"\n⚠️  Directory {project_path} already exists. Continue? (y/N): ")
                    if response.lower() != 'y':
                        print("❌ Project creation cancelled")
                        sys.exit(1)
                except EOFError:
                    print("\n❌ Error: No input available. Please run this wizard in an interactive terminal.")
                    print("💡 Use command line arguments: python tools/project_wizard.py --name PROJECT_NAME --type TYPE")
                    sys.exit(1)
        
        # Create deliverables structure
        deliverables_path = project_path / "deliverables"
        for subdir in ["src", "test", "docs"]:
            (deliverables_path / subdir).mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Created project structure at {project_path}")
    
    def _generate_prd(self, project_path: Path, project_name: str, app_type: str) -> None:
        """Generate PRD from template."""
        template_file = self.templates_path / f"{app_type}_prd_template.md"
        
        if not template_file.exists():
            print(f"⚠️  PRD template not found for {app_type}")
            return
        
        # Read template and replace project name
        with open(template_file, 'r') as f:
            content = f.read()
        
        content = content.replace("{PROJECT_NAME}", project_name)
        
        # Write PRD file
        prd_path = project_path / "deliverables" / "PRD.md"
        with open(prd_path, 'w') as f:
            f.write(content)
        
        print(f"📄 Generated PRD template: {prd_path}")
    
    def _setup_tech_stack(self, project_path: Path, tech_stack: Optional[Dict]) -> None:
        """Setup technology stack files."""
        if not tech_stack:
            return
        
        # Create requirements.txt with dependencies
        requirements_path = project_path / "deliverables" / "requirements.txt"
        
        dependencies = []
        if 'dependencies' in tech_stack:
            dependencies.extend(tech_stack['dependencies'])
        
        # Add frontend dependencies if present
        if 'frontend' in tech_stack.get('dependencies', {}):
            frontend_deps = tech_stack['dependencies']['frontend']
            dependencies.extend([f"# Frontend: {dep}" for dep in frontend_deps])
        
        # Add backend dependencies if present  
        if 'backend' in tech_stack.get('dependencies', {}):
            backend_deps = tech_stack['dependencies']['backend']
            dependencies.extend(backend_deps)
        
        if dependencies:
            with open(requirements_path, 'w') as f:
                f.write(f"# {tech_stack['name']} Dependencies\\n")
                f.write("\\n".join(dependencies))
            
            print(f"📦 Created requirements.txt with {len(dependencies)} dependencies")
    
    def _create_framework_link(self, project_path: Path) -> None:
        """Create link to framework for development guidance."""
        claude_md_path = project_path / "CLAUDE.md"
        
        # Create a CLAUDE.md that imports the framework development guide
        content = f"""# Development Guide

This project uses the Claude Code Automation Framework for systematic development.

## Framework Integration
@{self.framework_path}/core/development_guide.md

## Quick Start
1. Complete the PRD.md file in deliverables/
2. Use TodoWrite to plan implementation tasks
3. Follow the framework development workflow
4. Run tests with: python deliverables/test/run_tests.py

For detailed guidance, see the framework development guide.
"""
        
        with open(claude_md_path, 'w') as f:
            f.write(content)
        
        print(f"🔗 Created framework integration: {claude_md_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Claude Code Automation Framework - Project Wizard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/project_wizard.py                          # Interactive mode
  python tools/project_wizard.py --name my_app           # CLI tool with default type
  python tools/project_wizard.py --name my_api --type api_service   # REST API
  
Application types:
  web_app, cli_tool, api_service, ml_system, trading_dashboard
        """
    )
    
    parser.add_argument(
        "--name", 
        help="Project name (letters, numbers, hyphens, underscores only)"
    )
    parser.add_argument(
        "--type", 
        choices=["web_app", "cli_tool", "api_service", "ml_system", "trading_dashboard"],
        default="cli_tool",
        help="Application type (default: cli_tool)"
    )
    
    args = parser.parse_args()
    
    wizard = ProjectWizard(args)
    try:
        wizard.run()
    except KeyboardInterrupt:
        print("\\n\\n👋 Project creation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()