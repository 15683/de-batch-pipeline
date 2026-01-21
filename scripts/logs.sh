#!/bin/bash

finch compose -f docker-compose.yaml logs -f $1
