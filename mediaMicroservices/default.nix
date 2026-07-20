{ pkgs }:
let
    scripts = pkgs.callPackage ./scripts {};
in
{
    packages = {
        initMediaMicroservices = scripts;
    };
}
