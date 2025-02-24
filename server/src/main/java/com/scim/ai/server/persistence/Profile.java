package com.scim.ai.server.persistence;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Access;
import jakarta.persistence.AccessType;
import jakarta.persistence.Column;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;

@Entity(name = "Profile")
@Table(name = "profiles", schema = "customer_schema")
@Access(AccessType.FIELD)
public class Profile {
  // Add annotations for
  // profile_id
  // user_id
  // first_name
  // last_name
  // phone
  // address

  @Id
  @GeneratedValue(generator = "users_user_id_seq")
  @Column(name = "profile_id")
  private Long profileId;

  @Column(name = "user_id", nullable = false)
  private Long userId;

  @Column(name = "first_name", nullable = false)
  private String firstName;

  @Column(name = "last_name", nullable = false)
  private String lastName;

  @Column(name = "phone")
  private String phone;

  @Column(name = "address")
  private String address;

  public Long getProfileId() {
    return profileId;
  }

  public Long getUserId() {
    return userId;
  }

  public Profile setUserId(Long userId) {
    this.userId = userId;
    return this;
  }

  public String getFirstName() {
    return firstName;
  }

  public Profile setFirstName(String firstName) {
    this.firstName = firstName;
    return this;
  }

  public String getLastName() {
    return lastName;
  }

  public Profile setLastName(String lastName) {
    this.lastName = lastName;
    return this;
  }

  public String getPhone() {
    return phone;
  }

  public Profile setPhone(String phone) {
    this.phone = phone;
    return this;
  }

  public String getAddress() {
    return address;
  }

  public Profile setAddress(String address) {
    this.address = address;
    return this;
  }
}
