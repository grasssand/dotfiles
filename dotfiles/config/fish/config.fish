# https://github.com/CachyOS/cachyos-fish-config/blob/main/cachyos-config.fish

# Format man pages
set -gx MANROFFOPT "-c"
set -gx MANPAGER "sh -c 'col -bx | bat -l man -p --theme=\"OneHalfDark\"'"
if not type -q bat
    set -gx MANPAGER "less -R"
end

if status is-interactive
    # Init plugins
    starship init fish | source
    zoxide init fish | source
    fzf --fish | source

    # Plugins settings
    set -U __done_min_cmd_duration 10000
    set -U __done_notification_urgency_level low
    fzf_configure_bindings --variables=

    function backup --argument filename
        cp $filename $filename.bak
    end

    # Copy: 安全递归、保留属性、智能处理目录末尾 /
    function copy
        # 参数不足直接提示
        if test (count $argv) -lt 2
            echo "Usage: copy <source...> <dest>"
            return 1
        end

        # 取最后一个参数作为目标，其余为源
        set -l dest $argv[-1]
        set -l sources $argv[1..-2]

        set -l opts "-a"  # 保留权限/时间戳/符号链接

        # 检查是否为目录到目录的单源模式
        if test (count $sources) = 1; and test -d "$sources[1]"; and test -d "$dest"
            set sources (string trim -r -c '/' -- $sources[1])
        end

        # 防御：文件名可能以 - 开头 → 加 --
        command cp $opts -- $sources $dest
    end

    # 离开 Yazi 时更改工作目录
    function y
        set tmp (mktemp -t "yazi-cwd.XXXXXX")
        yazi $argv --cwd-file="$tmp"
        if read -z cwd < "$tmp"; and [ -n "$cwd" ]; and [ "$cwd" != "$PWD" ]
            builtin cd -- "$cwd"
        end
        rm -f -- "$tmp"
    end
end

## Useful aliases
# Replace ls with eza
alias l="eza -al --color=always --group-directories-first --icons"  # preferred listing
alias la="eza -al --color=always --group-directories-first --icons" # preferred listing
alias ls="eza -a --color=always --group-directories-first --icons"  # all files and dirs
alias ll="eza -l --color=always --group-directories-first --icons"  # long format
alias lt="eza -aT --color=always --group-directories-first --icons" # tree listing
alias l.="eza -a | grep -e '^\.'"                                   # show only dotfiles

alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ......="cd ../../../../.."

# Common use
alias fixpacman="sudo rm /var/lib/pacman/db.lck"
alias psmem="ps auxf | sort -nr -k 4"
alias psmem10="ps auxf | sort -nr -k 4 | head -10"
alias cleanup="sudo pacman -Rns (pacman -Qtdq)"             # Cleanup orphaned packages
alias jctl="journalctl -p 3 -xb"                            # Get the error messages from journalctl
alias cat="bat --paging=never"
alias cc="cliphist wipe"
alias x="extract"
