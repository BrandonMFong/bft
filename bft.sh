##
# author: brando
# date: 12/30/24

function bft-init() {
	if [ "$ZSH_VERSION" != "" ]; then
		SCRIPT_PATH=$(dirname $functions_source[$0])
	else
		SCRIPT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )	
	fi
	export PATH="$SCRIPT_PATH/pool/bin:$PATH";
	export PATH="$SCRIPT_PATH/src:$PATH";
	export PYTHONPATH="$SCRIPT_PATH/src:$PYTHONPATH";
}

bft-init;

