##
# author: brando
# date: 12/30/24

function bft-init() {
	SCRIPT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )	
	export PATH="$SCRIPT_PATH/pool/bin:$PATH";
	export PATH="$SCRIPT_PATH:$PATH";
}

bft-init;

