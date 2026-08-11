{
  description = "Nix flake for mazegen";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      systems = nixpkgs.lib.systems.flakeExposed;
      forEachSystem = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forEachSystem (pkgs: {
        default = pkgs.mkShellNoCC {
          packages = [
            pkgs.python313
            pkgs.uv
            pkgs.ruff
          ];
          env = {
            LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib ];
            UV_PYTHON_DOWNLOADS = "never";
            UV_PYTHON = "${pkgs.python313}/bin/python3.13";
          };
        };
      });
    };
}
