package com.example.demo.modules.company.service;

import javax.servlet.http.HttpServletResponse;
import java.io.UnsupportedEncodingException;

public interface CompanyService {

    void download(HttpServletResponse resp, String company) throws UnsupportedEncodingException;

    void download2(HttpServletResponse response, String comp);
}
