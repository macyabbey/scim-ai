package com.scim.ai.server.persistence;

import jakarta.persistence.Access;
import jakarta.persistence.AccessType;
import jakarta.persistence.Basic;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.NamedQueries;
import jakarta.persistence.NamedQuery;
import jakarta.persistence.Table;
import jakarta.persistence.GeneratedValue;

@Entity(name = "User")
@Table(name = "users", schema = "customer_schema")
@Access(AccessType.FIELD)
public class User {
  @Id
  @GeneratedValue(generator = "users_user_id_seq")
  @Column(name = "user_id", nullable = false)
  private Long userId;

  @Basic
  @Column(name = "username", nullable = false, length = 50)
  private String username;

  @Basic
  @Column(name = "email", nullable = false, length = 100)
  private String email;

  @Basic
  @Column(name = "role", nullable = false, length = 20)
  private String role;

  @Basic
  @Column(name = "created_at", nullable = false)
  private java.time.LocalDateTime createdAt;

  @Basic
  @Column(name = "last_login")
  private java.time.LocalDateTime lastLogin;

  public Long getUserId() {
    return userId;
  }

  public String getUsername() {
    return username;
  }

  public User setUsername(String username) {
    this.username = username;
    return this;
  }

  public String getEmail() {
    return email;
  }

  public User setEmail(String email) {
    this.email = email;
    return this;
  }

  public String getRole() {
    return role;
  }

  public User setRole(String role) {
    this.role = role;
    return this;
  }

  public java.time.LocalDateTime getCreatedAt() {
    return createdAt;
  }

  public User setCreatedAt(java.time.LocalDateTime createdAt) {
    this.createdAt = createdAt;
    return this;
  }

  public java.time.LocalDateTime getLastLogin() {
    return lastLogin;
  }

  public User setLastLogin(java.time.LocalDateTime lastLogin) {
    this.lastLogin = lastLogin;
    return this;
  }
}
