import matplotlib.pyplot as plt
import numpy as np
import util
import argparse
import os
from timeit import default_timer as timer

config = util.load_config()


def generated_and_save_chart(
    data: dict[dict],
    file_path: str,
    top_n: int = -1,
    title: str = "Usage",
    categories=config["ENTITY_COLS"] + ["not_included"],
    preserve_order: bool = False,
) -> None:
    plt.rcParams["figure.figsize"] = (14, 13)
    keywords = list(data.keys())
    if top_n != -1:
        if not preserve_order:
            keywords = {
                key: value
                for key, value in sorted(
                    data.items(), key=lambda item: sum(item[1].values()), reverse=True
                )
            }
        else:
            keywords = {key: value for key, value in data.items()}
        keywords = list(keywords.keys())[:top_n]

    occurrences = [sum(data[keyword].values()) for keyword in keywords]

    keywords = {
        keyword: {
            category: value / sum(data[keyword].values())
            for category, value in data[keyword].items()
        }
        for keyword in keywords
    }
    _, ax = plt.subplots()

    x = np.arange(len(keywords))
    width = 0.35

    bottom_values = [0] * len(keywords)

    # TODO: extract computation from this method
    for _, category in enumerate(categories):
        values = []
        for keyword in keywords:
            keyword_data = keywords[keyword]
            category_value = keyword_data.get(category, 0)
            values.append(category_value)
        ax.bar(x, values, width, label=category, bottom=bottom_values)
        bottom_values = [bottom_values[j] + values[j] for j in range(len(keywords))]

    ax.set_xlabel("Keywords")
    ax.set_ylabel("Ratio")
    ax.set_title(title)
    ax.set_xticks(x)
    plt.xticks(rotation=90)
        
    ax.set_xticklabels(
        [
            f"{keyword} ({occurrence})"
            for keyword, occurrence in zip(keywords, occurrences)
        ]
    )
    ax.legend(fancybox=True, framealpha=0.3)

    plt.savefig(file_path)
    print(f"Image saved to {file_path} successfully!")


def generate_filename(args, prefix):
    filename = f"{args.spec_name}_{prefix}"
    if args.filter_samples:
        filename += "_filtered"
        if args.only_rules is not None:
            if args.only_rules:
                filename += "_rules"
            else:
                filename += "_non_rules"
    else:
        filename += "_unfiltered"
    filename += f"_threshold{args.threshold}"
    filename += f"_top{args.top_n}words.png"

    return filename


def compute_multiple_categoried_keywords(hmap, sum_of_attributes, threshold):
    multiple_categoried_keywords = {
        keyword: attributes
        for keyword, attributes in hmap.items()
        if sum_of_attributes[keyword] != 0
        and attributes["not_included"] / sum_of_attributes[keyword] < threshold
        and sum([(val > 0) for _, val in attributes.items()])
        > 2  # at least 3 categories
    }

    multiple_categoried_keywords = {
        key: value
        for key, value in sorted(
            multiple_categoried_keywords.items(),
            key=lambda item: sum(item[1].values()),
            reverse=True,
        )
    }

    return multiple_categoried_keywords


def compute_most_conflicting_keywords(hmap, sum_of_attributes, threshold):
    def sort_hmap(hmap):
        def find_dominant_elements(subdict):
            max_value = max(subdict.values())
            dominant_elements = [
                key for key, value in subdict.items() if value == max_value
            ]
            total = sum(subdict.values())
            weight = max_value / total
            return dominant_elements, weight

        dominant_weights = {}
        for key, subdict in hmap.items():
            dominant_elements, weight = find_dominant_elements(subdict)
            dominant_weights[key] = (dominant_elements, weight)
        sorting_key = lambda item: (
            dominant_weights[item[0]][1],
            dominant_weights[item[0]][0],
        )
        return dict(sorted(hmap.items(), key=sorting_key))

    most_conflicting_words = {
        keyword: attributes
        for keyword, attributes in hmap.items()
        if sum_of_attributes[keyword] != 0
        and attributes["not_included"] / sum_of_attributes[keyword]
        < threshold  # should be included at least (1-threshold) of time it is seen
        and sum([(val > 0) for _, val in attributes.items()])
        > 1  # at least 2 categories
        and sum(attributes.values()) >= 8  # seen at least 8 times in the specification
    }

    most_conflicting_keywords = sort_hmap(most_conflicting_words)

    return most_conflicting_keywords


def run(args: argparse.Namespace):
    start = timer()

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    target = os.path.join(args.output_path, "keyword_analysis/")
    if not os.path.exists(target):
        os.makedirs(target)

    all_spec_names = config["FILENAMES"]
    all_spec_names = {k.lower(): v for k, v in all_spec_names.items()}
    filename = all_spec_names[args.spec_name]

    # analysis takes up to 8-10 minutes depending on the computation power
    if args.spec_name == "all":
        print(f"Analysis has started. It will take a few minutes.")

    data = util.read(
        filename=filename,
        filter_samples=args.filter_samples,
        only_rules=args.only_rules,
    )

    keywords = util.extract_keywords(df=data)
    hmap = util.compute_frequency_of_keywords(df=data, keywords=keywords)

    output_filename = generate_filename(args, "mostcommonkeywords")

    generated_and_save_chart(
        data=hmap,
        file_path=os.path.join(args.output_path, "keyword_analysis/", output_filename),
        top_n=args.top_n,
        title="Most used keywords",
    )

    # here, using sum_of_attrbs you could check typos (e.g. 'temprature' will have 0 as its sum of attributes)
    # attribute represents the columns (eg. im_keyword etc.)
    sum_of_attributes = util.extract_attributes(hmap)

    # filtering, can make the filtering more strict
    hmap_filtered = util.filter_hmap(
        hmap=hmap, sum_of_attributes=sum_of_attributes, threshold=args.threshold
    )

    output_filename = generate_filename(args, "filtered-mostcommonwords")
    generated_and_save_chart(
        data=hmap_filtered,
        file_path=os.path.join(args.output_path, "keyword_analysis/", output_filename),
        top_n=args.top_n,
        title="Most used keywords, filtered by inclusion",
    )

    multiple_categoried_keywords = compute_multiple_categoried_keywords(
        hmap, sum_of_attributes, threshold=args.threshold
    )

    output_filename = generate_filename(args, "multiple-category-keywords")
    generated_and_save_chart(
        data=multiple_categoried_keywords,
        file_path=os.path.join(args.output_path, "keyword_analysis/", output_filename),
        top_n=args.top_n,
        title="Keywords assigned to more than 2 categories",
    )

    most_conflicting_keywords = compute_most_conflicting_keywords(
        hmap, sum_of_attributes, args.threshold
    )

    output_filename = generate_filename(args, "most-conflicting-keywords")
    generated_and_save_chart(
        data=most_conflicting_keywords,
        file_path=os.path.join(args.output_path, "keyword_analysis/", output_filename),
        top_n=args.top_n,
        title="Most conflicting keywords",
        preserve_order=True,
    )

    end = timer()
    print(f"Analysis took {end-start} seconds.")


if __name__ == "__main__":
    _parser = argparse.ArgumentParser("")

    _parser.add_argument(
        "-f",
        "--filter_samples",
        help="flag indicating if filtering is active",
        action=argparse.BooleanOptionalAction,
        default=False,
    )

    sentence_filter_group = _parser.add_mutually_exclusive_group()

    sentence_filter_group.add_argument(
        "--only_rule_sentences",
        action=argparse.BooleanOptionalAction,
        help="filter by only rule sentences",
        default=False,
    )

    sentence_filter_group.add_argument(
        "--only_non_rule_sentences",
        action=argparse.BooleanOptionalAction,
        help="filter by only non-rule sentences",
        default=False,
    )

    _parser.add_argument(
        "-s",
        "--spec_name",
        help="which specification to run analysis on - default: all",
        default="all",
        choices=[
            "all",
            "autoid",
            "iolink",
            "isa95",
            "machinetools",
            "mv1ccm",
            "mv2amcm",
            "packml",
            "padim",
            "profinet",
            "robotics",
            "uafx",
            "weihenstephan",
        ],
    )

    _parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        help="output directory where file will be saved in",
        default="output/",
    )

    _parser.add_argument(
        "-n", "--top_n", type=int, help="amount of displayed words", default=20
    )

    _parser.add_argument(
        "-t", "--threshold", type=float, help="inclusion threshold", default="0.9"
    )

    args = _parser.parse_args()

    if args.filter_samples and not (
        args.only_rule_sentences or args.only_non_rule_sentences
    ):
        _parser.error(
            "When using -f, either --only_rule_sentences or --only_non_rule_sentences is required."
        )

    # bool
    args.only_rules = args.filter_samples and args.only_rule_sentences

    run(args)
