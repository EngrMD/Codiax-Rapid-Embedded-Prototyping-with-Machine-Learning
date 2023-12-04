#!/bin/bash

# Check if pyenv is installed
if command -v pyenv &>/dev/null; then
    echo "pyenv is already installed. Run the next part of the installation"
else
    # Install pyenv
    echo "Installing pyenv..."
    curl https://pyenv.run | bash

    # Add pyenv to the shell
    if [ -n "$BASH_VERSION" ]; then
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
        echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    elif [ -n "$ZSH_VERSION" ]; then
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
        echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
        echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
    fi

    echo "pyenv installed successfully."
fi

# Restart the shell to apply the changes in Python version
if [ -n "$ZSH_VERSION" ]; then
    exec zsh
elif [ -n "$BASH_VERSION" ]; then
    exec "$SHELL"
else
    exec "$SHELL"
fi
