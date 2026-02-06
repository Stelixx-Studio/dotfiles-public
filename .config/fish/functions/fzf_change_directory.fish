function _fzf_change_directory
    fzf | perl -pe 's/([ ()])/\\\\$1/g' | read foo
    if test -n "$foo"
        builtin cd $foo
        commandline -r ''
        commandline -f repaint
    else
        commandline ''
    end
end

function fzf_change_directory --description "Fuzzy find and change directory across projects"
    begin
        echo $HOME/.config
        # Find all git repos in ghq
        find (ghq root) -maxdepth 4 -type d -name .git 2>/dev/null | sed 's/\/\.git//'
        # Current directory subdirectories
        ls -ad */ 2>/dev/null | perl -pe "s#^#$PWD/#" | grep -v \.git
        # Developments directory (if exists)
        test -d $HOME/Developments; and ls -ad $HOME/Developments/*/* 2>/dev/null | grep -v \.git
    end | sed -e 's/\/$//' | awk '!a[$0]++' | _fzf_change_directory $argv
end
