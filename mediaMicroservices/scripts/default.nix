{ pkgs, stdenv }:
let
    movieInfo = stdenv.mkDerivation {
        name = "mm-write-movie-info";
        dontUnpack = true;

        buildInputs = with pkgs; [
            makeWrapper
            (python3.withPackages (py-pkgs: with py-pkgs; [ aiohttp ]))
        ];

        installPhase = ''
            install -Dm555 ${./write_movie_info.py} $out/bin/mm-write-movie-info
        '';
    };
in pkgs.writeScriptBin "init-media-microservices" ''
    #!/usr/bin/env bash
    script=$(basename "''${BASH_SOURCE[0]}")

    USAGE="
    Usage: $script <web-server> 

    Args: 
        web-server: connection string to the webserver. E.g.: localhost:8080
    "

    if (( $# != 1 )); then
        echo "$USAGE"
        exit 1
    fi

    ${movieInfo}/bin/mm-write-movie-info -c ${./../datasets/tmdb/casts.json} -m ${./../datasets/tmdb/movies.json} --server_address "http://$1"
''
