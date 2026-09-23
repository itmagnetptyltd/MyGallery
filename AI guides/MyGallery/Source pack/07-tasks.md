# Candidate task inventory

Mined from the test suite, which is written in the user's verbs by people who knew the intended flow. Rewrite each title into the reader's goal, verb-first, then group by goal area. Test coverage is not task coverage, so this is a start and not the inventory.

## Candidate goal areas, from test grouping

| Group | Candidate chapter | Reference |
| --- | --- | --- |

## From end-to-end tests

| Test title | Rewritten as a task | Reader group | Frequency | Reference |
| --- | --- | --- | --- | --- |
| test_following_the_documented_start_steps_displays_the_gallery |  |  |  | tests/e2e/test_boot.py:21 |
| test_the_gallery_page_is_titled_for_the_application |  |  |  | tests/e2e/test_boot.py:28 |
| test_every_card_shows_download_and_delete_without_hovering |  |  |  | tests/e2e/test_card_actions_browser.py:39 |
| test_a_cards_download_and_delete_are_the_same_width |  |  |  | tests/e2e/test_card_actions_browser.py:59 |
| test_downloading_from_a_card_delivers_that_photo_without_the_larger_view |  |  |  | tests/e2e/test_card_actions_browser.py:71 |
| test_deleting_from_a_card_asks_first_without_the_larger_view |  |  |  | tests/e2e/test_card_actions_browser.py:88 |
| test_declining_a_delete_from_a_card_keeps_the_photo |  |  |  | tests/e2e/test_card_actions_browser.py:101 |
| test_confirming_a_delete_from_a_card_removes_that_card |  |  |  | tests/e2e/test_card_actions_browser.py:112 |
| test_asking_to_delete_a_photo_asks_for_confirmation |  |  |  | tests/e2e/test_delete_browser.py:34 |
| test_the_confirmation_asks_are_you_sure_you_want_to_delete_this_photo |  |  |  | tests/e2e/test_delete_browser.py:44 |
| test_declining_the_confirmation_leaves_the_photo_in_the_gallery |  |  |  | tests/e2e/test_delete_browser.py:57 |
| test_confirming_the_deletion_removes_the_thumbnail_from_the_gallery |  |  |  | tests/e2e/test_delete_browser.py:70 |
| test_confirming_the_deletion_leaves_the_other_thumbnails |  |  |  | tests/e2e/test_delete_browser.py:83 |
| test_choosing_a_file_shows_a_preview_image_before_the_upload_is_made |  |  |  | tests/e2e/test_description_browser.py:57 |
| test_choosing_thirty_files_shows_a_preview_for_every_one |  |  |  | tests/e2e/test_description_browser.py:71 |
| test_a_description_given_with_the_upload_reaches_the_gallery |  |  |  | tests/e2e/test_description_browser.py:83 |
| test_an_upload_with_no_description_still_adds_the_photo |  |  |  | tests/e2e/test_description_browser.py:96 |
| test_the_description_field_holds_250_characters_and_the_upload_is_not_refused |  |  |  | tests/e2e/test_description_browser.py:106 |
| test_dropping_files_on_the_popup_chooses_them_for_the_upload |  |  |  | tests/e2e/test_description_browser.py:122 |
| test_a_thumbnail_carries_its_photos_description_as_alt_text |  |  |  | tests/e2e/test_description_browser.py:135 |
| test_a_thumbnail_with_no_description_carries_its_filename_as_alt_text |  |  |  | tests/e2e/test_description_browser.py:147 |
| test_a_description_is_changed_in_the_larger_view |  |  |  | tests/e2e/test_description_browser.py:160 |
| test_typing_one_character_shows_one_of_two_hundred_and_fifty |  |  |  | tests/e2e/test_description_browser.py:172 |
| test_typing_a_forty_first_character_shows_forty_one_of_two_hundred_and_fifty |  |  |  | tests/e2e/test_description_browser.py:182 |
| test_each_preview_renders_its_own_file |  |  |  | tests/e2e/test_description_browser.py:195 |
| test_downloading_from_a_card_delivers_a_file |  |  |  | tests/e2e/test_download_browser.py:31 |
| test_the_downloaded_file_is_named_as_it_was_uploaded |  |  |  | tests/e2e/test_download_browser.py:42 |
| test_the_downloaded_file_holds_the_bytes_that_were_uploaded |  |  |  | tests/e2e/test_download_browser.py:53 |
| test_an_empty_gallery_shows_no_thumbnail |  |  |  | tests/e2e/test_gallery_browser.py:27 |
| test_an_empty_gallery_says_there_are_no_photos_yet |  |  |  | tests/e2e/test_gallery_browser.py:34 |
| test_an_empty_gallery_shows_the_upload_control |  |  |  | tests/e2e/test_gallery_browser.py:41 |
| test_an_empty_gallery_reports_no_error |  |  |  | tests/e2e/test_gallery_browser.py:48 |
| test_uploaded_photos_appear_as_thumbnails |  |  |  | tests/e2e/test_gallery_browser.py:60 |
| test_the_no_photos_message_goes_once_a_photo_is_uploaded |  |  |  | tests/e2e/test_gallery_browser.py:69 |
| test_thumbnails_appear_newest_first |  |  |  | tests/e2e/test_gallery_browser.py:78 |
| test_no_numbered_page_control_is_shown |  |  |  | tests/e2e/test_gallery_browser.py:89 |
| test_scrolling_to_the_end_loads_more_thumbnails |  |  |  | tests/e2e/test_gallery_browser.py:98 |
| test_the_larger_view_shows_save_description_and_close_side_by_side |  |  |  | tests/e2e/test_larger_view_actions_browser.py:29 |
| test_the_close_button_closes_the_larger_view |  |  |  | tests/e2e/test_larger_view_actions_browser.py:48 |
| test_the_larger_view_is_not_shown_before_a_thumbnail_is_activated |  |  |  | tests/e2e/test_larger_view_browser.py:23 |
| test_activating_a_thumbnail_shows_the_larger_view |  |  |  | tests/e2e/test_larger_view_browser.py:31 |
| test_the_larger_view_shows_the_photo_that_was_activated |  |  |  | tests/e2e/test_larger_view_browser.py:41 |
| test_the_photo_is_rendered_larger_than_its_thumbnail |  |  |  | tests/e2e/test_larger_view_browser.py:59 |
| test_pressing_escape_closes_the_larger_view |  |  |  | tests/e2e/test_larger_view_browser.py:72 |
| test_the_gallery_is_shown_again_after_escape |  |  |  | tests/e2e/test_larger_view_browser.py:84 |
| test_activating_the_close_control_closes_the_larger_view |  |  |  | tests/e2e/test_larger_view_browser.py:95 |
| test_the_gallery_is_shown_again_after_the_close_control |  |  |  | tests/e2e/test_larger_view_browser.py:107 |
| test_the_gallery_keeps_its_scroll_position_when_the_larger_view_closes |  |  |  | tests/e2e/test_larger_view_browser.py:118 |
| test_a_photo_smaller_than_its_thumbnail_is_still_rendered_larger |  |  |  | tests/e2e/test_larger_view_small_photo_browser.py:52 |
| test_a_photo_narrower_than_the_panel_is_centred_in_it |  |  |  | tests/e2e/test_larger_view_small_photo_browser.py:74 |
| test_a_thumbnail_card_is_wider_than_160_pixels |  |  |  | tests/e2e/test_uat_visual_browser.py:55 |
| test_a_thumbnail_is_shown_as_a_card_not_a_bare_image |  |  |  | tests/e2e/test_uat_visual_browser.py:67 |
| test_starting_an_upload_opens_a_popup |  |  |  | tests/e2e/test_uat_visual_browser.py:80 |
| test_an_empty_gallery_shows_a_control_that_opens_the_upload_popup |  |  |  | tests/e2e/test_uat_visual_browser.py:92 |
| test_the_close_control_is_inside_the_larger_view_panel |  |  |  | tests/e2e/test_uat_visual_browser.py:106 |
| test_the_upload_popup_close_control_is_inside_the_popup_at_its_top_right |  |  |  | tests/e2e/test_uat_visual_browser.py:127 |
| test_closing_the_upload_popup_adds_no_photo |  |  |  | tests/e2e/test_uat_visual_browser.py:146 |
| test_the_upload_popup_can_be_reopened_after_it_was_closed |  |  |  | tests/e2e/test_uat_visual_browser.py:158 |
| test_the_upload_popup_previews_every_chosen_file |  |  |  | tests/e2e/test_uat_visual_browser.py:170 |
| test_a_thumbnail_shows_its_photos_description_as_alt_text |  |  |  | tests/e2e/test_uat_visual_browser.py:187 |
| test_the_picker_still_chooses_files_when_dropping_is_available |  |  |  | tests/e2e/test_uat_visual_browser.py:201 |
| test_the_gallery_is_shown_without_a_sign_in_step |  |  |  | tests/e2e/test_upload.py:20 |
| test_uploading_a_photo_through_the_browser_adds_it_to_the_gallery |  |  |  | tests/e2e/test_upload.py:27 |
| test_uploading_a_batch_through_the_browser_adds_every_photo |  |  |  | tests/e2e/test_upload.py:40 |
| test_a_batch_with_three_failures_keeps_the_photos_that_worked |  |  |  | tests/e2e/test_upload_failures_browser.py:36 |
| test_each_failed_file_is_named_on_the_page |  |  |  | tests/e2e/test_upload_failures_browser.py:47 |
| test_each_failure_shows_its_reason_beside_its_name |  |  |  | tests/e2e/test_upload_failures_browser.py:60 |
| test_an_oversized_file_names_the_25_mb_limit_on_the_page |  |  |  | tests/e2e/test_upload_failures_browser.py:71 |
| test_the_upload_popup_is_wider_than_680_pixels_on_a_1280_pixel_screen |  |  |  | tests/e2e/test_upload_popup_look_browser.py:79 |
| test_the_upload_popup_close_control_looks_like_the_larger_views |  |  |  | tests/e2e/test_upload_popup_look_browser.py:93 |
| test_the_upload_popup_has_the_larger_view_panels_border |  |  |  | tests/e2e/test_upload_popup_look_browser.py:104 |
| test_choose_files_and_upload_look_like_save_description |  |  |  | tests/e2e/test_upload_popup_look_browser.py:115 |
| test_a_wide_preview_is_as_wide_as_the_description_field |  |  |  | tests/e2e/test_upload_preview_size_browser.py:54 |
| test_a_preview_keeps_its_images_proportions |  |  |  | tests/e2e/test_upload_preview_size_browser.py:61 |
| test_a_narrow_preview_is_centred_in_the_popup |  |  |  | tests/e2e/test_upload_preview_size_browser.py:70 |

## From other tests, lower yield

| Test title | Reference |
| --- | --- |
| test_requesting_the_root_path_serves_the_gallery_page | tests/test_app.py:5 |
| test_the_gallery_page_presents_the_gallery_region | tests/test_app.py:12 |
| test_the_gallery_page_is_served_as_html | tests/test_app.py:18 |
| test_the_gallery_page_is_served_with_a_content_security_policy | tests/test_app.py:26 |
| test_the_gallery_page_is_served_with_nosniff | tests/test_app.py:45 |
| test_a_started_server_reports_a_loopback_bound_address | tests/test_binding.py:14 |
| test_a_started_server_refuses_a_connection_to_the_machine_network_address | tests/test_binding.py:23 |
| test_a_thumbnail_card_is_built_with_download_and_delete_controls | tests/test_card_actions.py:22 |
| test_the_card_controls_share_the_row_in_equal_columns | tests/test_card_actions.py:33 |
| test_the_server_is_configured_to_listen_on_loopback_only | tests/test_config.py:5 |
| test_the_configured_port_matches_the_port_in_the_start_instructions | tests/test_config.py:12 |
| test_deleting_a_photo_removes_it_from_the_gallery | tests/test_delete.py:13 |
| test_deleting_a_photo_leaves_the_other_photos | tests/test_delete.py:22 |
| test_deleting_a_photo_removes_its_file_from_disk | tests/test_delete.py:33 |
| test_deleting_a_photo_removes_its_thumbnail_from_disk | tests/test_delete.py:43 |
| test_deleting_a_photo_that_is_not_there_is_refused | tests/test_delete.py:52 |
| test_a_photo_uploaded_with_a_description_carries_it | tests/test_description.py:13 |
| test_a_photo_uploaded_with_no_description_carries_none_and_is_still_a_photo | tests/test_description.py:20 |
| test_changing_a_description_replaces_it_and_leaves_the_photo_itself_unchanged | tests/test_description.py:30 |
| test_a_photo_carrying_no_description_can_be_given_one | tests/test_description.py:41 |
| test_changing_the_description_of_a_photo_that_is_not_there_is_refused | tests/test_description.py:50 |
| test_an_upload_with_no_description_still_becomes_a_photo | tests/test_description.py:60 |
| test_a_description_of_250_characters_is_carried_whole | tests/test_description.py:68 |
| test_a_photo_listed_in_a_page_carries_its_description | tests/test_description.py:77 |
| test_a_gallery_written_before_descriptions_existed_is_still_readable | tests/test_description.py:86 |
| test_a_usable_filename_is_delivered_unchanged | tests/test_download.py:19 |
| test_an_empty_filename_falls_back_to_the_identifier | tests/test_download.py:24 |
| test_a_filename_of_only_spaces_falls_back | tests/test_download.py:29 |
| test_a_filename_containing_a_path_is_refused | tests/test_download.py:38 |
| test_a_filename_containing_a_control_character_is_refused | tests/test_download.py:47 |
| test_a_fallback_name_ends_in_the_extension_for_the_format | tests/test_download.py:58 |
| test_a_photo_is_still_in_the_gallery_later_in_the_same_run | tests/test_durability.py:20 |
| test_deleting_one_photo_leaves_the_other_in_the_gallery | tests/test_durability.py:27 |
| test_a_photo_is_still_in_the_gallery_when_the_store_is_reopened | tests/test_durability.py:37 |
| test_a_photo_is_present_in_the_storage_folder_as_a_readable_file | tests/test_durability.py:44 |
| test_the_stored_file_holds_the_bytes_that_were_uploaded | tests/test_durability.py:53 |
| test_a_deleted_photo_is_still_gone_when_the_store_is_reopened | tests/test_durability.py:63 |
| test_a_description_given_at_upload_survives_a_restart | tests/test_durability.py:75 |
| test_a_description_changed_after_upload_survives_a_restart | tests/test_durability.py:82 |
| test_a_description_removed_after_upload_stays_removed_across_a_restart | tests/test_durability.py:90 |
| test_a_photo_uploaded_before_descriptions_existed_is_shown_carrying_none | tests/test_durability.py:98 |
| test_photos_are_listed_with_the_most_recently_uploaded_first | tests/test_gallery.py:16 |
| test_a_page_holds_no_more_than_the_page_size | tests/test_gallery.py:25 |
| test_a_page_of_a_long_gallery_is_not_the_whole_gallery | tests/test_gallery.py:32 |
| test_the_next_page_continues_where_the_previous_one_ended | tests/test_gallery.py:41 |
| test_a_page_reports_no_cursor_once_the_gallery_is_exhausted | tests/test_gallery.py:51 |
| test_an_empty_gallery_holds_no_photos | tests/test_gallery.py:61 |
| test_reading_an_empty_gallery_raises_no_error | tests/test_gallery.py:66 |
| test_a_gallery_that_cannot_be_read_reports_a_failure | tests/test_gallery.py:71 |
| test_the_application_issues_an_identifier | tests/test_identity.py:7 |
| test_two_photos_uploaded_under_the_same_filename_get_different_identifiers | tests/test_identity.py:12 |
| test_an_identifier_contains_no_path_separator | tests/test_identity.py:20 |
| test_requesting_a_photo_returns_the_bytes_that_were_uploaded | tests/test_larger_view.py:22 |
| test_requesting_a_photo_returns_it_as_an_image | tests/test_larger_view.py:32 |
| test_the_photo_served_is_larger_than_its_thumbnail | tests/test_larger_view.py:42 |
| test_requesting_an_unknown_photo_is_not_found | tests/test_larger_view.py:51 |
| test_the_larger_view_actions_are_save_description_and_close | tests/test_larger_view_actions.py:14 |
| test_the_application_is_launched_at_the_address_the_instructions_name | tests/test_launcher.py:20 |
| test_starting_the_application_binds_it_to_loopback | tests/test_launcher.py:27 |
| test_starting_the_application_listens_on_the_documented_port | tests/test_launcher.py:37 |
| test_starting_the_application_opens_the_browser_at_the_gallery | tests/test_launcher.py:47 |
| test_the_start_instructions_name_exactly_one_prerequisite | tests/test_start_instructions.py:9 |
| test_the_named_prerequisite_is_python | tests/test_start_instructions.py:14 |
| test_the_start_instructions_reach_a_running_application_in_a_single_step | tests/test_start_instructions.py:19 |
| test_the_documented_start_file_exists | tests/test_start_instructions.py:24 |
| test_saving_a_photo_puts_it_in_the_gallery | tests/test_store.py:7 |
| test_saving_a_second_photo_leaves_the_first_in_place | tests/test_store.py:14 |
| test_a_saved_photo_can_be_retrieved_afterwards | tests/test_store.py:22 |
| test_a_retrieved_photo_carries_the_bytes_that_were_saved | tests/test_store.py:29 |
| test_two_photos_saved_under_the_same_filename_get_different_identifiers | tests/test_store.py:37 |
| test_a_photo_keeps_the_filename_it_was_uploaded_under | tests/test_store.py:45 |
| test_a_filename_containing_path_separators_stores_inside_the_photo_directory | tests/test_store.py:52 |
| test_a_filename_containing_a_drive_letter_stores_inside_the_photo_directory | tests/test_store.py:61 |
| test_a_thumbnail_is_smaller_in_bytes_than_its_photo | tests/test_thumbnails.py:12 |
| test_a_thumbnail_renders_its_own_photo_and_not_another | tests/test_thumbnails.py:20 |
| test_every_photo_in_the_gallery_has_a_thumbnail | tests/test_thumbnails.py:34 |
| test_gallery_css_sets_card_min_width_above_160px | tests/test_uat_visual.py:26 |
| test_gallery_html_has_a_card_surface_around_each_thumbnail | tests/test_uat_visual.py:32 |
| test_gallery_html_includes_an_upload_popup | tests/test_uat_visual.py:41 |
| test_empty_gallery_html_includes_a_control_that_opens_the_upload_popup | tests/test_uat_visual.py:53 |
| test_larger_view_markup_places_close_inside_the_panel | tests/test_uat_visual.py:61 |
| test_a_thumbnails_alt_text_is_its_photos_description | tests/test_uat_visual.py:79 |
| test_the_upload_popup_has_a_close_control | tests/test_uat_visual.py:88 |
| test_the_upload_popup_close_control_is_inside_the_popup | tests/test_uat_visual.py:96 |
| test_the_upload_popup_close_control_is_placed_at_the_top_right | tests/test_uat_visual.py:107 |
| test_the_upload_popup_close_control_closes_the_popup | tests/test_uat_visual.py:120 |
| test_the_upload_popup_shows_a_preview_of_each_chosen_file | tests/test_uat_visual.py:129 |
| test_the_upload_popup_accepts_dropped_files | tests/test_uat_visual.py:140 |
| test_dropping_on_the_upload_popup_is_not_the_only_way_to_choose | tests/test_uat_visual.py:148 |
| test_closing_the_upload_popup_leaves_it_reusable | tests/test_uat_visual.py:160 |
| test_the_upload_popup_shows_a_character_count_for_the_description | tests/test_uat_visual.py:176 |
| test_the_character_count_reads_its_limit_from_the_field | tests/test_uat_visual.py:183 |
| test_an_interrupted_save_adds_no_photo | tests/test_upload_failures.py:33 |
| test_an_interrupted_save_leaves_no_photo_file | tests/test_upload_failures.py:43 |
| test_an_interrupted_save_leaves_no_thumbnail | tests/test_upload_failures.py:53 |
| test_an_interrupted_save_leaves_no_temp_file | tests/test_upload_failures.py:63 |
| test_opening_the_store_removes_a_file_that_has_no_row | tests/test_upload_failures.py:79 |
| test_the_too_large_reason_names_the_25_mb_limit | tests/test_upload_failures.py:91 |
| test_the_upload_popup_is_wider_than_the_delivered_680_pixels | tests/test_upload_popup_look.py:38 |
| test_the_upload_popup_and_larger_view_share_one_close_control_rule | tests/test_upload_popup_look.py:49 |

55 further rows omitted. The complete set is in `harvest.json`.
