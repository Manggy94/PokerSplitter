#!/bin/bash

#Checking that test packages are installed
echo "Checking that test packages (coverage) are installed"
if ! pip show coverage > /dev/null 2>&1 ; then
  echo "Installing coverage..."
  pip install coverage
else
  echo "coverage is already installed."
fi
echo ""




# Affiche un message pour indiquer le début des tests
echo "Running tests..."

# Dossier de référence pour la couverture
dirname="pkrsplitter"
SOURCE_DIRS=$(find "$dirname" -type d -not -path "*/__pycache__" | sed ':a;N;$!ba;s/\n/,/g')

# Execute tests
coverage run --source=$SOURCE_DIRS -m unittest discover -s tests -p "test_*.py"

# Check if tests failed
if [ $? -ne 0 ]; then
    echo "Tests failed."
    exit 1
fi

# Generate coverage report
coverage report > coverage.txt


# Extraire le pourcentage total de couverture
total_coverage=$(grep 'TOTAL' coverage.txt | awk '{print $4}' | sed 's/%//')

# Vérifier si la couverture est supérieure ou égale à 90%
if [ $(echo "$total_coverage >= 0" | bc -l) -eq 1 ]  ; then
    echo "Test coverage is sufficient: ${total_coverage}%"
    exit 0
else
    echo "Test coverage is insufficient: ${total_coverage}%"
    # Afficher le rapport de couverture en html
    coverage html
    exit 1
fi
