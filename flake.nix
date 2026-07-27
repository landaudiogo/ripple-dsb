{
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
    };
    outputs = { self, nixpkgs, ... }:
        let
            system = "x86_64-linux";
            pkgs = import nixpkgs { inherit system; };
            socialNetwork = pkgs.callPackage ./socialNetwork {};
            mediaMicroservices = pkgs.callPackage ./mediaMicroservices {};
            tag = self.shortRev or self.dirtyShortRev;
        in {
            packages.${system} = {
                socialNetwork.initSocialGraph = socialNetwork.packages.initSocialGraph;
                mediaMicroservices.initMediaMicroservices = mediaMicroservices.packages.initMediaMicroservices;
            };
            images.${system} = {
                socialNetwork.initSocialGraph = pkgs.dockerTools.buildImage {
                    name = "initSocialGraph";
                    inherit tag;
                    copyToRoot = [ self.packages.${system}.socialNetwork.initSocialGraph ];
                    config = {
                        Entrypoint = [ "/bin/sn-init-social-graph" ];
                    };
                };
                mediaMicroservices.initMediaMicroservices = pkgs.dockerTools.buildImage {
                    name = "initMediaMicroservices";
                    inherit tag;
                    copyToRoot = [ self.packages.${system}.mediaMicroservices.initMediaMicroservices ];
                    config = {
                        Entrypoint = [ "/bin/init-media-microservices" ];
                    };
                };
            };
        };
}

