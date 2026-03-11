# Fallback for terminals that do not render Nerd Font glyphs correctly (e.g. Codex app terminal).
# Keep full icons for normal terminals; use ASCII in AI-runtime terminals to avoid tofu squares.
if set -q CODEX_SHELL
    set -g tide_git_icon git
    set -g tide_os_icon mac
    set -g tide_pwd_icon dir
    set -g tide_pwd_icon_home '~'
    set -g tide_pwd_icon_unwritable '!'
    set -g tide_node_icon node
    set -g tide_python_icon py
    set -g tide_ruby_icon rb
    set -g tide_java_icon java
    set -g tide_go_icon go
    set -g tide_rustc_icon rs
    set -g tide_docker_icon docker
    set -g tide_kubectl_icon k8s
    set -g tide_terraform_icon tf
    set -g tide_aws_icon aws
    set -g tide_gcloud_icon gcp
    set -g tide_jobs_icon jobs
    set -g tide_cmd_duration_icon took
    set -g tide_character_icon '>'
    set -g tide_character_vi_icon_default '<'
    set -g tide_character_vi_icon_replace '>'

    # Codex terminal still renders some Tide glyphs as tofu after reload.
    # Use a guaranteed ASCII prompt here to avoid any font-dependent symbols.
    function fish_prompt --description 'ASCII prompt for Codex terminal'
        set -l last_status $status
        set -l cwd (prompt_pwd)
        set -l vcs (fish_vcs_prompt)

        set_color brgreen
        echo -n $cwd
        set_color normal

        if test -n "$vcs"
            echo -n " $vcs"
        end

        if test $last_status -ne 0
            set_color red
            echo -n " !"$last_status
            set_color normal
        end

        echo -n " > "
    end

    function fish_right_prompt --description 'Disable right prompt in Codex terminal'
    end
end
