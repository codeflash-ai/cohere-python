class CohereObject:
    def __repr__(self) -> str:
        # exclude_list and type name computation maintained as before
        exclude_list = ["iterator"]
        type_name = type(self).__name__

        # Build list of lines more efficiently (avoids string concatenation in loop)
        contents_lines = [f"\t{k}: {v}\n" for k, v in self.__dict__.items() if k not in exclude_list]
        # Join all lines in one efficient call
        contents = "".join(contents_lines)

        output = f"cohere.{type_name} {{\n{contents}}}"
        return output
