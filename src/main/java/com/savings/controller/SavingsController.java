package com.savings.controller;

import com.savings.entity.Customers;
import com.savings.repository.CustomerRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@Slf4j

public class SavingsController {

    @Autowired
    CustomerRepository cr;

    @PostMapping("/saveAccounts")
    public void addCustomers(@RequestBody List<Customers> customer) {
        log.info("Adding customer list :" + customer);
        cr.saveAll(customer);

    }
}
