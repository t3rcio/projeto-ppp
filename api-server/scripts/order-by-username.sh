#!/bin/bash

ARG_ASC="-asc"
ARG_DESC="-desc"

function help(){
    # Exibe o texto de ajuda do script
    echo
    echo "Use: order-by-username [input] [options]: Retorna a lista ordenada"
    echo "Options:"
    echo "    no options: Retorna a lista ordenada CRESCENTE"
    echo "    -asc: Retorna a lista em ordem CRESCENTE"
    echo "    -desc: Retorna a lista em ordem DECRESCENTE"
    echo
    exit

}
if [ "$1" == '' ] || [ "$1" == 'help' ]; then
    help
fi

case $2 in
    
    "help")
    help
    ;;
    
    "$ARG_ASC" | "")
        sort -k1 $1
    ;;

    "$ARG_DESC")
        sort -r -k1 $1
    ;;
esac
