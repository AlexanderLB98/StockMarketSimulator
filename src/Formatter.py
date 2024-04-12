
class Formatter:
    @staticmethod
    def format_response(response):
        if isinstance(response, dict):
            return Formatter.format_dict(response)
        elif isinstance(response, str):
            return response
        elif isinstance(response, list):
            return Formatter.format_list(response)
        else:
            return str(response)

    @staticmethod
    def format_dict(dictionary):
        formatted_lines = [f"{key}: {value}" for key, value in dictionary.items()]
        return "\n".join(formatted_lines)

    @staticmethod
    def format_list(lst):
        formatted_lines = [str(item) for item in lst]
        return "\n".join(formatted_lines)
