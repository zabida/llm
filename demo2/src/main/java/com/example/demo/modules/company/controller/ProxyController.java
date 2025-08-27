package com.example.demo.modules.company.controller;


import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.util.StreamUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.Collections;

@RestController
public class ProxyController {

    @Value("${flask.base-url:http://192.168.10.102:5000}")
    private String flaskBaseUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    @RequestMapping("/**")
    public ResponseEntity<?> proxy(HttpServletRequest request) throws IOException {
        String method = request.getMethod();

        // 拼接目标 URL，带 query string
        StringBuilder targetUrl = new StringBuilder(flaskBaseUrl).append(request.getRequestURI());
        if (request.getQueryString() != null) {
            targetUrl.append("?").append(request.getQueryString());
        }

        // 打印日志方便调试
        System.out.println(">>> Forwarding " + method + " " + targetUrl);

        // 复制 Headers
        HttpHeaders headers = new HttpHeaders();
        Collections.list(request.getHeaderNames()).forEach(name ->
                headers.add(name, request.getHeader(name)));

        // 复制 Body（仅对有请求体的方法）
        byte[] body = StreamUtils.copyToByteArray(request.getInputStream());
        HttpEntity<byte[]> entity = new HttpEntity<>(body, headers);

        // 转发请求
        ResponseEntity<byte[]> response =
                restTemplate.exchange(targetUrl.toString(), HttpMethod.resolve(method), entity, byte[].class);

        // 返回响应
        return ResponseEntity.status(response.getStatusCode())
                .headers(response.getHeaders())
                .body(response.getBody());
    }
}