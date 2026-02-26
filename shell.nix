let
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-25.11";
  pkgs = import nixpkgs { config = {}; overlays = []; };
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    
    # Comment out ollama and uncomment its rocm or cuda variant for gpu acceleration 
    ollama
    #ollama-rocm
    #ollama-cuda
    python312
    python312Packages.ollama
    python312Packages.huggingface-hub
    python312Packages.pandas
    python312Packages.pyarrow

    tmux
  ];

  OLLAMA_HOST="127.0.0.1:11435";
  OLLAMA_MODELS="models";

  shellHook = ''ollama serve &>/dev/null &'';
}
