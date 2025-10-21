warning = "AWS dependencies are not installed. Please install boto3, botocore, and sagemaker."


def lazy_sagemaker():
    try:
        import sagemaker  # type: ignore
    except ImportError:
        from cohere.manually_maintained.lazy_aws_deps import warning

        raise ImportError(warning)
    return sagemaker


def lazy_boto3():
    try:
        import boto3  # type: ignore

        return boto3
    except ImportError:
        raise ImportError(warning)


def lazy_botocore():
    try:
        import botocore  # type: ignore

        return botocore
    except ImportError:
        raise ImportError(warning)
