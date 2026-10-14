from job_mcp.browser.guard import classify_click, classify_key
from job_mcp.tests.fixtures.factories import make_element


def test_should_block_click_when_button_says_submit_application():
    assert not classify_click(make_element(text="Submit application")).allowed


def test_should_block_click_when_submit_button_says_apply_on_a_filled_form():
    assert not classify_click(make_element(type="submit", text="Apply", form_fields=9)).allowed


def test_should_block_click_when_unlabeled_submit_button_is_on_a_large_form():
    assert not classify_click(make_element(type="submit", text="", form_fields=6)).allowed


def test_should_allow_click_when_link_opens_the_application():
    assert classify_click(make_element(tag="a", text="Apply for this job", in_form=False, form_fields=0)).allowed


def test_should_allow_click_when_easy_apply_button_is_outside_a_form():
    assert classify_click(make_element(text="Easy Apply", in_form=False, form_fields=0)).allowed


def test_should_allow_click_when_submit_button_moves_to_next_step():
    assert classify_click(make_element(type="submit", text="Next", form_fields=12)).allowed


def test_should_allow_click_when_submit_button_is_a_small_search_form():
    assert classify_click(make_element(type="submit", text="Search", form_fields=2)).allowed


def test_should_block_click_when_button_text_hides_submit_inside_review_label():
    assert not classify_click(make_element(text="Review and submit")).allowed


def test_should_block_enter_when_focus_is_a_plain_form_field():
    assert not classify_key("Enter", make_element(tag="input", type="text", text="")).allowed


def test_should_allow_enter_when_focus_is_a_combobox():
    assert classify_key("Enter", make_element(tag="input", role="combobox")).allowed


def test_should_block_key_when_not_on_allowed_list():
    assert not classify_key("Control+Enter", make_element()).allowed
