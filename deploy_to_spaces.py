#!/usr/bin/env python3
"""
Deploy AI Executive Agent to Hugging Face Spaces
Automated deployment script
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(step, text):
    """Print step"""
    print(f"{step}. {text}")

def run_command(cmd, description):
    """Run shell command"""
    print(f"   Running: {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   ❌ Error: {result.stderr}")
        return False
    print(f"   ✅ Done")
    return True

def main():
    """Main deployment function"""
    print_header("🚀 AI Executive Agent - Spaces Deployment")
    
    # Check if in correct directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found. Run from project root.")
        sys.exit(1)
    
    # Get Hugging Face username
    username = input("Enter your Hugging Face username: ").strip()
    if not username:
        print("❌ Username required")
        sys.exit(1)
    
    space_name = "ai-executive-agent"
    
    print_step(1, "Preparing deployment files")
    
    # Create deployment directory
    deploy_dir = Path("deploy_spaces")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Copy essential files
    files_to_copy = [
        "app.py",
        "requirements-spaces.txt",
        "Dockerfile.spaces",
        "README_SPACES.md",
        ".dockerignore"
    ]
    
    dirs_to_copy = [
        "api",
        "core",
        "config",
        "dashboard"
    ]
    
    print("   Copying files...")
    for file in files_to_copy:
        if Path(file).exists():
            dest = deploy_dir / file
            shutil.copy2(file, dest)
            print(f"   ✅ Copied {file}")
    
    # Rename for Spaces
    (deploy_dir / "Dockerfile.spaces").rename(deploy_dir / "Dockerfile")
    (deploy_dir / "requirements-spaces.txt").rename(deploy_dir / "requirements.txt")
    (deploy_dir / "README_SPACES.md").rename(deploy_dir / "README.md")
    
    print("   Copying directories...")
    for dir_name in dirs_to_copy:
        if Path(dir_name).exists():
            shutil.copytree(dir_name, deploy_dir / dir_name)
            print(f"   ✅ Copied {dir_name}/")
    
    print("   ✅ All files prepared")
    
    print_step(2, "Checking Hugging Face CLI")
    
    # Check if huggingface_hub is installed
    try:
        import huggingface_hub
        print("   ✅ huggingface_hub installed")
    except ImportError:
        print("   Installing huggingface_hub...")
        if not run_command("pip install huggingface_hub", "Install huggingface_hub"):
            sys.exit(1)
    
    print_step(3, "Creating Space")
    
    print(f"""
   Creating Space: {username}/{space_name}
   
   You need to:
   1. Login to Hugging Face (if not already)
   2. Confirm space creation
   
   Press Enter to continue...
   """)
    input()
    
    # Login
    print("   Logging in to Hugging Face...")
    os.system("huggingface-cli login")
    
    # Create space
    create_cmd = f'huggingface-cli repo create {space_name} --type space --space_sdk docker -y'
    print(f"   Creating space...")
    os.system(create_cmd)
    
    print_step(4, "Uploading files")
    
    # Change to deploy directory
    os.chdir(deploy_dir)
    
    # Initialize git
    run_command("git init", "Initialize git")
    run_command("git add .", "Stage files")
    run_command('git commit -m "Deploy AI Executive Agent"', "Commit files")
    
    # Add remote and push
    repo_url = f"https://huggingface.co/spaces/{username}/{space_name}"
    run_command(f"git remote add space {repo_url}", "Add remote")
    
    print("   Pushing to Hugging Face...")
    os.system(f"git push space main --force")
    
    # Go back
    os.chdir("..")
    
    print_step(5, "Configuration")
    
    print(f"""
   ✅ Space created successfully!
   
   🔗 URL: https://huggingface.co/spaces/{username}/{space_name}
   
   ⚙️  Next Steps:
   
   1. Go to your Space settings:
      https://huggingface.co/spaces/{username}/{space_name}/settings
   
   2. Add Environment Variables:
      - GOOGLE_API_KEY (required) - Get from https://makersuite.google.com/app/apikey
      - COMET_API_KEY (optional)
      - OPIK_API_KEY (optional)
   
   3. Wait for build (3-5 minutes)
   
   4. Access your dashboard!
   
   📚 Documentation:
   - See SPACES_DEPLOYMENT.md for detailed guide
   - Check build logs if deployment fails
   
   """)
    
    # Cleanup
    print("   Cleaning up deployment files...")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    
    print_header("🎉 Deployment Complete!")
    print(f"Visit: https://huggingface.co/spaces/{username}/{space_name}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
