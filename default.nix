with import <nixpkgs> {}; {
  pyEnv = stdenv.mkDerivation {
    name = "nixos";
    buildInputs = [
      stdenv
      python3Full
      python3Packages.virtualenv
      libxml2
    ];
    LIBRARY_PATH="${libxml2}/lib";
    shellHook = ''
      unset http_proxy
      export GIT_SSL_CAINFO=/etc/ssl/certs/ca-bundle.crt
      export SSL_CERT_FILE=${cacert}/etc/ssl/certs/ca-bundle.crt
    '';
  };
}
