{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell {
  packages = with pkgs; [
    termshark
    tcpdump
  ];
  buildInputs = with pkgs; [
    (python313.withPackages (
      ps: with ps; [
        pip
      ]
    ))
  ];

  shellHook = ''
    python -m venv .venv
    source .venv/bin/activate  
    pip install -r requirements.txt
    LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/
  '';
}
