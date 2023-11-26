#!/bin/bash


function test(){
 local NUM='1'
}

# NUM not available yet.
echo "This is NUM before funct call:  $NUM"

test
echo "This is NUM after funct call:  $NUM"
