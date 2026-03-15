#!/bin/bash
# Git LFS 配置脚本

echo "=== Git LFS 配置指南 ==="
echo ""

# 检查是否已安装
check_git_lfs() {
    if command -v git-lfs &> /dev/null; then
        echo "✓ Git LFS 已安装: $(git-lfs version)"
        return 0
    else
        echo "✗ Git LFS 未安装"
        return 1
    fi
}

# 安装指南
install_guide() {
    echo ""
    echo "请根据你的系统安装Git LFS:"
    echo ""
    echo "macOS:"
    echo "  brew install git-lfs"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install git-lfs"
    echo ""
    echo "CentOS/RHEL:"
    echo "  sudo yum install git-lfs"
    echo ""
    echo "Windows:"
    echo "  1. 访问 https://git-lfs.github.com/"
    echo "  2. 下载安装包并运行"
    echo ""
    echo "安装完成后，运行: git lfs install"
}

# 配置项目的Git LFS
setup_project() {
    echo ""
    echo "=== 配置项目Git LFS ==="
    
    # 初始化Git LFS
    git lfs install
    
    # 追踪所有OBJ文件
    git lfs track "*.obj"
    
    # 创建.gitattributes
    cat > .gitattributes << 'GITATTR'
# 自动追踪所有OBJ文件
*.obj filter=lfs diff=lfs merge=lfs -text
GITATTR
    
    echo ""
    echo "✓ Git LFS 配置完成"
    echo ""
    echo "生成的文件:"
    echo "  - .gitattributes (追踪规则)"
    echo ""
    echo "下一步:"
    echo "  1. git add .gitattributes"
    echo "  2. git commit -m 'Add Git LFS tracking for OBJ files'"
    echo "  3. git add partof_BP3D_4.0_obj_99/"
    echo "  4. git commit -m 'Add 3D models via Git LFS'"
    echo ""
    echo "注意: HTML文件不需要修改！"
}

# 主流程
if check_git_lfs; then
    setup_project
else
    install_guide
    echo ""
    echo "安装完成后，重新运行此脚本: bash setup-git-lfs.sh"
fi
