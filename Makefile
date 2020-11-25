.PHONY: generate
generate:
	poetry run python -m grpc_tools.protoc --python_betterproto_out=flow_py_sdk/proto -I ./proto ./proto/flow/**/*.proto
