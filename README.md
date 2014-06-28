# INSTRUCTIONS

1. Install XCODE and XCODE command tools

2. Clone this repo to into your home folder.
    - git clone https://github.com/msalvadores/dotfiles.git ~/.dotfiles
    - cd ~/.dotfiles; git submodule init; git submodule update

3. Install brew
    - ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

4. oh-my-zsh
    - git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
    - chsh -s /bin/zsh

5. Install brew, cask and pip apps
    - cd apps; ./install\_apps

6. Set links
    - ./setlinks

7. In OSX
    - cd osx; ./defaults

# EXTRA

For patched fonts follow instructions here:

http://superuser.com/questions/762345/powerline-patched-fonts-on-osx-10-9-3-iterm2-chrome
