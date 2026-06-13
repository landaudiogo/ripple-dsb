{
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
    };
    outputs = { self, nixpkgs, ... }:
        let
            system = "x86_64-linux";
            pkgs = import nixpkgs { inherit system; };
            socialNetwork = pkgs.callPackage ./socialNetwork {};
        in {
            packages.${system} = {
                socialNetwork.initSocialGraph = socialNetwork.packages.initSocialGraph;
            };
        };
}

