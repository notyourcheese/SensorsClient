.PHONY: help setup env configure run clean

VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python

# Show help
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

# Setup project: venv + dependencies ## Set up the virtual environment and install requirements
setup: $(VENV_DIR)/bin/activate requirements.txt ## Create venv and install dependencies
	@echo "[✓] Virtualenv and dependencies installed."
	@make env

$(VENV_DIR)/bin/activate:
	@echo "[•] Creating virtual environment..."
	@python3 -m venv $(VENV_DIR)
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install -r requirements.txt

env: ## Create .env from template if it doesn't exist
	@if [ ! -f .env ]; then \
		echo "[•] Creating .env from .env.template..."; \
		cp .env.template .env; \
	else \
		echo "[✓] .env already exists. Skipping."; \
	fi

smart-configure: ## Prompt for each variable in .env.template and create .env
	@echo "[•] Generating .env interactively from .env.template..."
	@touch .env
	@> .env
	@cat .env.template | while IFS= read -r line; do \
		case $$line in \
			""|\#*) \
				echo "$$line" >> .env ;; \
			*=*) \
				key=$$(echo "$$line" | cut -d= -f1); \
				default=$$(echo "$$line" | cut -d= -f2-); \
				read -p "$$key [default: $$default]: " val; \
				val=$${val:-$$default}; \
				echo "$$key=$$val" >> .env ;; \
			*) \
				echo "$$line" >> .env ;; \
		esac \
	done
	@echo "[✓] .env created with your inputs."


configure: ## Interactively create a .env file with sensor config
	@echo "[•] Interactive .env configuration..."
	@read -p "Sensor types to use (DHT22,DHT11,DS18B20): " types; \
	read -p "DHT22 pin (e.g., D24): " dht22_pin; \
	read -p "DHT11 pin (e.g., D23): " dht11_pin; \
	read -p "DS18B20 ID (e.g., 28-xxxxxxxxxxxx): " ds18b20_id; \
	echo "SENSOR_TYPES=$$types" > .env; \
	echo "DHT22_PIN=$$dht22_pin" >> .env; \
	echo "DHT11_PIN=$$dht11_pin" >> .env; \
	echo "DS18B20_ID=$$ds18b20_id" >> .env; \
	echo "[✓] .env created with your configuration."

run: ## Run the sensor reader
	@$(PYTHON) -m src.main

clean: ## Remove virtual environment
	rm -rf $(VENV_DIR)
