{
  description = "CRD extractor shell script with dependencies";

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

        pythonWithPackages = pkgs.python3.withPackages (ps:
          with ps; [
            pyyaml
          ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonWithPackages
            pkgs.bash
            pkgs.coreutils
            pkgs.curl
            pkgs.findutils
            pkgs.gnused
            pkgs.kubectl
            pkgs.just
            pkgs.yq-go
            pkgs.vendir
          ];
        };
      }
    );
}
