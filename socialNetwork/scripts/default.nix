{ pkgs, stdenv }:
let
    datasets = stdenv.mkDerivation {
        name = "graph-datasets";
        dontUnpack = true;
        installPhase = ''
            cp -r ${../datasets/social-graph} $out
        '';
    };
in
stdenv.mkDerivation {
    name = "sn-init-social-graph";
    dontUnpack = true;

    buildInputs = with pkgs; [
        makeWrapper
        (python3.withPackages (py-pkgs: with py-pkgs; [ aiohttp ]))
    ];

    installPhase = ''
        install -Dm555 ${./init_social_graph.py} $out/bin/sn-init-social-graph
        wrapProgram $out/bin/sn-init-social-graph --set GRAPH_DATASETS "${datasets}"
    '';
}
