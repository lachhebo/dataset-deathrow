PHONY: update the datasets on kaggle
update:
      source deathrow/bin/activate
      kaggle datasets version -p datasets -m "update data"
