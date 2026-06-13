{ pkgs }:
let
    scripts = pkgs.callPackage ./scripts {};
in
{
    packages = {
        initSocialGraph = scripts;
    };
}
