#!/usr/bin/env python3
"""
🚀 Automated Hugging Face Spaces Deployment Script
This script automates the deployment process to Hugging Face Spaces
"""
import os
import subprocess
import sys
from pathlib import Path
import shutil

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(step_num, message):
    """Print a step message"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}[{step_num}] {message}{Colors.ENDC}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def run_command(cmd, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    """Main deployment function"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*60}")
    print("🚀 AI Executive Agent - Hugging Face Spaces Deployment")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    # Get project root
    project_root = Path(__file__).parent
    
    # Step 1: Get Space URL
    print_step(1, "Hugging Face Space Configuration")
    print("\nPlease enter your Hugging Face Space URL:")
    print("Example: https://huggingface.co/spaces/YOUR_USERNAME/ai-executive-agent")
    space_url = input(f"{Colors.CYAN}Space URL: {Colors.ENDC}").strip()
    
    if not space_url or "huggingface.co/spaces/" not in space_url:
        print_error("Invalid Space URL!")
        sys.exit(1)
    
    # Extract username and space name
    parts = space_url.split("huggingface.co/spaces/")[1].split("/")
    username = parts[0]
    space_name = parts[1] if len(parts) > 1 else "ai-executive-agent"
    
    print_success(f"Space: {username}/{space_name}")
    
    # Step 2: Create deployment directory
    print_step(2, "Preparing deployment files")
    deploy_dir = project_root / "deploy_temp"
    
    if deploy_dir.exists():
        print_warning("Removing existing deployment directory...")
        shutil.rmtree(deploy_dir)
    
    deploy_dir.mkdir()
    print_success("Deployment directory created")
    
    # Step 3: Copy necessary files
    print_step(3, "Copying project files")
    
    # Files and directories to copy
    items_to_copy = [
        "app.py",
        "api",
        "core",
        "config",
        "dashboard",
        ".dockerignore",
    ]
    
    for item in items_to_copy:
        src = project_root / item
        dst = deploy_dir / item
        
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            print_success(f"Copied directory: {item}")
        elif src.is_file():
            shutil.copy2(src, dst)
            print_success(f"Copied file: {item}")
        else:
            print_warning(f"Skipped (not found): {item}")
    
    # Step 4: Copy and rename Spaces-specific files
    print_step(4, "Configuring Spaces-specific files")
    
    # Copy Dockerfile
    shutil.copy2(
        project_root / "Dockerfile.spaces",
        deploy_dir / "Dockerfile"
    )
    print_success("Configured Dockerfile")
    
    # Copy requirements
    shutil.copy2(
        project_root / "requirements-spaces.txt",
        deploy_dir / "requirements.txt"
    )
    print_success("Configured requirements.txt")
    
    # Copy README
    shutil.copy2(
        project_root / "README_SPACES.md",
        deploy_dir / "README.md"
    )
    print_success("Configured README.md")
    
    # Step 5: Initialize git repository
    print_step(5, "Initializing Git repository")
    
    success, output = run_command("git init", cwd=deploy_dir)
    if success:
        print_success("Git repository initialized")
    else:
        print_error("Failed to initialize Git")
        print(output)
        sys.exit(1)
    
    # Step 6: Add Hugging Face remote
    print_step(6, "Adding Hugging Face remote")
    
    remote_url = f"https://huggingface.co/spaces/{username}/{space_name}"
    success, output = run_command(f"git remote add origin {remote_url}", cwd=deploy_dir)
    if success:
        print_success(f"Remote added: {remote_url}")
    else:
        print_warning("Remote might already exist")
    
    # Step 7: Commit files
    print_step(7, "Committing files")
    
    run_command("git add .", cwd=deploy_dir)
    success, output = run_command(
        'git commit -m "🚀 Deploy AI Executive Agent to Hugging Face Spaces"',
        cwd=deploy_dir
    )
    if success:
        print_success("Files committed")
    else:
        print_error("Failed to commit files")
        print(output)
        sys.exit(1)
    
    # Step 8: Push to Hugging Face
    print_step(8, "Pushing to Hugging Face Spaces")
    print("\n" + "="*60)
    print(f"{Colors.YELLOW}⚠️  You will need to authenticate with Hugging Face{Colors.ENDC}")
    print("="*60)
    print("\nOptions:")
    print("1. Use Hugging Face token (recommended)")
    print("2. Use SSH key")
    print("\nFor token authentication:")
    print("  Username: Your HF username")
    print("  Password: Your HF token (get from: https://huggingface.co/settings/tokens)")
    
    input(f"\n{Colors.CYAN}Press Enter when ready to push...{Colors.ENDC}")
    
    success, output = run_command("git push -u origin main --force", cwd=deploy_dir)
    
    if success or "Everything up-to-date" in output:
        print_success("Successfully pushed to Hugging Face Spaces! 🎉")
    else:
        print_error("Failed to push to Hugging Face")
        print(output)
        print("\n" + "="*60)
        print(f"{Colors.YELLOW}Troubleshooting:{Colors.ENDC}")
        print("1. Make sure your Hugging Face token has write access")
        print("2. Try manually: cd deploy_temp && git push origin main")
        print("3. Check: https://huggingface.co/settings/tokens")
        print("="*60)
    
    # Step 9: Environment variables reminder
    print_step(9, "⚠️ Important: Configure Environment Variables")
    print("\n" + "="*60)
    print(f"{Colors.YELLOW}Don't forget to set these in Space Settings:{Colors.ENDC}")
    print("="*60)
    print(f"\n{Colors.BOLD}Required:{Colors.ENDC}")
    print("  GOOGLE_API_KEY=your_gemini_api_key")
    print(f"\n{Colors.BOLD}Optional:{Colors.ENDC}")
    print("  COMET_API_KEY=your_comet_key")
    print("  OPIK_API_KEY=your_opik_key")
    print("\n" + "="*60)
    
    # Final message
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}")
    print("✅ Deployment Complete!")
    print(f"{'='*60}{Colors.ENDC}\n")
    print(f"Your Space: {Colors.CYAN}{space_url}{Colors.ENDC}")
    print(f"\nNext steps:")
    print(f"1. Go to: {space_url}/settings")
    print(f"2. Add environment variables (especially GOOGLE_API_KEY)")
    print(f"3. Wait for build to complete (~5-10 minutes)")
    print(f"4. Visit: {space_url}")
    print(f"\n{Colors.GREEN}🎉 Happy deploying!{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Deployment cancelled by user.{Colors.ENDC}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.ENDC}\n")
        sys.exit(1)
