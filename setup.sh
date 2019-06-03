#!/bin/bash

TEMPLATES=()
TEMPLATE=""
for dir in ./templates/*/; do
  TEMPLATES+=("$(basename $dir)")
done
TEMPLATES+=('quit')

function has_value() {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && echo "0" && return; done
  echo "1"
}

function better_select() {
  printf "$1"
  OPTIONS="${@:2}"
  id=1
  for op in ${OPTIONS[@]}; do
    printf "\033[1;90m%d)\033[0m %s\n" $id "$op"
    id=$((id+1))
  done
  id=$((id-1))
  while [[ 1 ]]; do
    printf "\033[90m>>\033[0m "
    read num
    if [[ $num -ge 1 ]] && [[ $num -lt $id ]]; then
      return $((num-1))
    elif [[ $num == $id ]]; then
      printf "Quiting"
      exit 0
    fi
  done
}

function select_template() {
  printf "\033[1;96mSelect template generator\033[0m\n"
  PS3=">> "
  select tem in ${TEMPLATES[@]}; do
    case $tem in
      "quit")
        echo "Canceling"
        exit 0
        ;;
      *)
        if ! [[ -z "$tem" ]]; then
          TEMPLATE="$tem"
          break
        fi
        ;;
    esac
  done
}

if [[ -z "$1" ]] || [[ $(has_value "$1" "${TEMPLATES[@]}") == "1" ]]; then
  better_select "\033[1;96mSelect template generator\033[0m\n" "${TEMPLATES[@]}"
  TEMPLATE=${TEMPLATES[$?]}
  # select_template
else
  TEMPLATE="$1"
fi

printf "\033[1;96mConstructing new $TEMPLATE project\033[0m\n"

printf "\033[1;13m  Setting template properties\033[0m\n"
