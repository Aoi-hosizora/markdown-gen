from md_toc import *


def build_toc(content: str) -> str:
    """
    Add toc to given content.
    """
    ordered = False
    no_links = False
    no_indentation = False
    no_list_coherence = False
    keep_header_levels = 3
    parser = 'github'
    list_marker = '-'

    toc = str()
    header_type_counter = dict()
    header_type_curr = 0
    header_type_prev = 0
    header_type_first = 0
    header_duplicate_counter = dict()

    if (ordered and list_marker == md_parser[parser]['list']['unordered']['default marker']):
        list_marker = md_parser[parser]['list']['ordered']['default closing marker']
    indentation_log = init_indentation_log(parser, list_marker)
    if not no_indentation and not no_list_coherence:
        indentation_list = init_indentation_status_list(parser)
    is_within_code_fence = False
    code_fence = None
    is_document_end = False

    for line in content.split('\n'):
        line += '\n'
        # Code fence detection.
        if is_within_code_fence:
            is_within_code_fence = not is_closing_code_fence(
                line, code_fence, is_document_end, parser)
        else:
            code_fence = is_opening_code_fence(line, parser)
            if code_fence is not None:
                # Update the status of the next line.
                is_within_code_fence = True

        if not is_within_code_fence or code_fence is None:
            # Header detection and gathering.
            header = get_md_header(line, header_duplicate_counter,
                                   keep_header_levels, parser, no_links)
            if header is not None:
                header_type_curr = header['type']

                # Take care of the ordered TOC.
                if ordered:
                    increase_index_ordered_list(header_type_counter,
                                                header_type_prev,
                                                header_type_curr, parser)
                    index = header_type_counter[header_type_curr]
                else:
                    index = 1

                # Take care of list indentations.
                if no_indentation:
                    no_of_indentation_spaces_curr = 0
                    # TOC list coherence checks are not necessary
                    # without indentation.
                else:
                    if not no_list_coherence:
                        if header_type_first == 0:
                            header_type_first = header_type_curr
                        if not toc_renders_as_coherent_list(
                                header_type_curr, header_type_first,
                                indentation_list, parser):
                            raise TocDoesNotRenderAsCoherentList

                    compute_toc_line_indentation_spaces(
                        header_type_curr, header_type_prev, parser, ordered,
                        list_marker, indentation_log, index)
                    no_of_indentation_spaces_curr = indentation_log[
                        header_type_curr]['indentation spaces']

                # Build a single TOC line.
                toc_line_no_indent = build_toc_line_without_indentation(
                    header, ordered, no_links, index, parser, list_marker)

                # Save the TOC line with the indentation.
                toc += build_toc_line(toc_line_no_indent,
                                      no_of_indentation_spaces_curr) + '\n'

                header_type_prev = header_type_curr

    return toc
