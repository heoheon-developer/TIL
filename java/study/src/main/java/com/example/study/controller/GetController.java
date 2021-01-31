package com.example.study.controller;


import com.example.study.model.SearchParam;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class GetController {

    @RequestMapping(method = RequestMethod.GET, path = "/getMethod")
    public String GetRequest() {

        return "Hi GetMethod";
    }

    @GetMapping("/getParameter")
    public String getParameter(@RequestParam String id, @RequestParam(name = "password") String pwd) {

        String password = "bbbb";

        System.out.println("id :" + id);
        System.out.println("pwd :" + pwd);
        return id + password;
    }

    @GetMapping("/getMultiParameter")
    public SearchParam GetMultiParameter(SearchParam searchParam) {

        System.out.println(searchParam.getAccount());
        System.out.println(searchParam.getEmail());
        System.out.println(searchParam.getPage());



        return searchParam;
    }


}


