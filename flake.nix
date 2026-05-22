{
  description = "k8s-schemas build environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3.withPackages (ps: with ps; [pyyaml]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.just
            pkgs.vendir
          ];
        };
      }
    );
}
