{
  pkgs ? import <nixpkgs> { },
}:
pkgs.mkShell rec {
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
    zlib
    glib
  ];

  shellHook = ''
    python -m venv .venv
    source .venv/bin/activate  
    pip install -r requirements.txt
    LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath buildInputs}:$LD_LIBRARY_PATH"
    LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/:$LD_LIBRARY_PATH"
  '';
}
