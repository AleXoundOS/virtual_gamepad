{
  description = "virtual gamepad shell";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pythonEnv = pkgs.python3.withPackages(ps: with pkgs.python3Packages; [ pynput python-uinput ]);
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          pythonEnv
        ];
      };
    };
  nixConfig.bash-prompt-suffix = "[devshell] ";
}
