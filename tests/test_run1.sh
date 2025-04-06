if [[ ${1} == "--verbose" ]]; then
    VERBOSE="--verbose"
else
    VERBOSE=""
fi

python -m pipenv run python src/main.py --books ${VERBOSE}