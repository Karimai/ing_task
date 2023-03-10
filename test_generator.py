import json

from publisher import SampleGenerator


def test_bad_sample_generator():
    """
    even though there are two samples data in the baddata.json file,
    only one of them is valid and should be returned.
    """
    sample_generator = SampleGenerator(faker=True, source="baddata.json")
    samples_counter = 0
    for sample in sample_generator.start():
        samples_counter += 1
        sample = json.loads(sample)
        assert type(sample) == dict
    assert samples_counter == 1  # Only one entity should be parsed
