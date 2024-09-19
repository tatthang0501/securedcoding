package com.sg.poc.domain.dto;

import java.util.List;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import lombok.Data;

@Data
public class SearchRequest {

  private Filter filter;
  private Pagination pagination;
  @NotNull(message = "Email cannot be null")
  @Pattern(regexp = "^[a-zA-Z0-9 ]+$", message = "Name must only contain letters, numbers, and spaces.")
  private String query;
  private String sorting;
  private List<String> returnFilterable;
  private String block;
  private String slug;
  private String terminalCode;

  @Data
  private static class Filter {

    private List<String> attributes;
  }

  @Data
  private static class Pagination {

    private Integer itemsPerPage;
    private Integer pageNumber;
  }

}
