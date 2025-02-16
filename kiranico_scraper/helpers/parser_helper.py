def content_container(heading, response, additional_path='/'):
    return response.xpath(f"//div[@class='element-wrapper' and descendant::h6[@class='element-header' and contains(text(), '{heading}')]]{additional_path}div[@class='table-responsive']")
