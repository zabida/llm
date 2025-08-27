package com.example.demo.modules.company.service.impl;

import com.example.demo.modules.company.service.CompanyService;
import com.itextpdf.text.DocumentException;
import com.itextpdf.text.pdf.AcroFields;
import com.itextpdf.text.pdf.BaseFont;
import com.itextpdf.text.pdf.PdfReader;
import com.itextpdf.text.pdf.PdfStamper;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletResponse;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import static javax.xml.transform.OutputKeys.ENCODING;


@Service
public class CompanyServiceImpl implements CompanyService {

    @Override
    public void download(HttpServletResponse response, String company) throws UnsupportedEncodingException {
        byte[] bytes = this.getTempFile("protocol.pdf", company);
        response.reset();
        response.setHeader("Content-Type", "application/octet-stream;charset=utf-8");
        response.setContentType(MediaType.parseMediaType("application/pdf").toString());
        response.addHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode("书上服务协议.pdf", "utf-8"));
        try(OutputStream os = response.getOutputStream()){
            os.write(bytes);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public byte[] getTempFile(String name, String comp){
        ClassPathResource classPathResource;
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();

        classPathResource = new ClassPathResource("templates/" + name);
        try {
            //BaseFont font = BaseFont.createFont();
            BaseFont font =  BaseFont.createFont("STSong-Light",
                    "UniGB-UCS2-H", BaseFont.NOT_EMBEDDED);
            PdfReader reader = new PdfReader(classPathResource.getPath());
            PdfStamper stamper = new PdfStamper(reader,outputStream);
            AcroFields form = stamper.getAcroFields();
            form.addSubstitutionFont(font);
            form.setField("company", comp);
            stamper.setFormFlattening(true);
            stamper.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return outputStream.toByteArray();
    }

    public void download2(HttpServletResponse response, String comp){
        try {
            response.reset();
            response.setHeader("Content-Type", "application/octet-stream;charset=utf-8");
            response.addHeader("Content-Disposition", "attachment;filename=" + URLEncoder.encode("书上服务协议.zip", "utf-8"));
            OutputStream os = response.getOutputStream();
            ZipOutputStream outputStream = new ZipOutputStream(os);

            outputStream.putNextEntry(new ZipEntry("protocol_in.pdf"));
            byte[] bytes = this.getTempFile("protocol.pdf", comp);
            outputStream.write(bytes);
            outputStream.closeEntry();

            outputStream.putNextEntry(new ZipEntry("pands_手册.pdf"));
            byte[] bytes2 = this.getTempFile("pandas.pdf", comp);
            outputStream.write(bytes2);
            outputStream.closeEntry();

            outputStream.close();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
