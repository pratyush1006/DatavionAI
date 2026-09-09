/**
 * =============================================================================
 * DatavionOS
 * File: src/core/api/client.ts
 * =============================================================================
 *
 * Central HTTP client for DatavionOS.
 *
 * Responsibilities
 * ----------------
 * - Configure Axios
 * - Provide typed HTTP methods
 * - Validate the DatavionOS API envelope
 * - Normalize transport/API errors
 * - Install request interceptors
 * - Install authentication response interceptors
 * - Support runtime authentication and tenant dependencies
 *
 * This module owns the HTTP transport implementation.
 *
 * Application-level singleton ownership belongs to:
 *
 *     @/core/api/factory.ts
 *
 * Design Principles
 * -----------------
 * - Single HTTP boundary
 * - Dependency inversion
 * - Strong TypeScript typing
 * - Backend contract aligned
 * - No feature-specific business logic
 * - SSR safe
 * - Enterprise Ready
 *
 * =============================================================================
 */

import axios, {
  AxiosError,
  type AxiosInstance,
  type AxiosResponse,
} from "axios";

import type {
  ApiError,
  ApiErrorResponse,
  ApiMeta,
  ApiRequestOptions,
  ApiResponse,
  ApiSuccessResponse,
  JsonValue,
} from "@/core/types";

import {
  createRequestInterceptor,
  installResponseInterceptors,
} from "./interceptors";

import type {
  ApiAuthenticationDependencies,
  ApiRuntimeDependencies,
} from "./contracts";

import {
  DEFAULT_REQUEST_ID_PROVIDER,
  EMPTY_TENANT_PROVIDER,
  EMPTY_TOKEN_PROVIDER,
} from "./contracts";

/* =============================================================================
 * Public Types
 * =============================================================================
 */

/**
 * API client configuration.
 *
 * This intentionally mirrors the canonical ApiConfig contract so the
 * application-level API configuration can be passed directly to ApiClient.
 */
export type ApiClientConfig =
  import("./config").ApiConfig;

/**
 * Axios request configuration with DatavionOS-specific controls.
 *
 * Axios owns generic request options such as:
 *
 * - method
 * - params
 * - timeout
 * - signal
 * - responseType
 *
 * DatavionOS owns:
 *
 * - skipAuth
 * - skipTenant
 * - skipRequestId
 */
export interface ApiRequestConfig
  extends Omit<
    import("axios").AxiosRequestConfig,
    "headers"
  >,
    ApiRequestOptions {
  readonly headers?: Record<
    string,
    string
  >;
}

/**
 * Normalized DatavionOS API exception.
 */
export class ApiClientError extends Error {
  public readonly code: string;

  public readonly statusCode: number;

  public readonly details: JsonValue;

  public readonly meta: ApiMeta | null;

  public readonly response:
    | AxiosResponse
    | null;

  public constructor(
    error: ApiError,
    options: {
      readonly statusCode: number;
      readonly meta?: ApiMeta | null;
      readonly response?:
        | AxiosResponse
        | null;
    },
  ) {
    super(error.message);

    this.name =
      "ApiClientError";

    this.code =
      error.code;

    this.statusCode =
      options.statusCode;

    this.details =
      error.details;

    this.meta =
      options.meta ?? null;

    this.response =
      options.response ?? null;

    Object.setPrototypeOf(
      this,
      new.target.prototype,
    );
  }
}

/* =============================================================================
 * API Client
 * =============================================================================
 */

/**
 * Canonical DatavionOS HTTP client.
 *
 * This class owns HTTP transport behavior.
 *
 * Application singleton ownership does NOT belong here.
 *
 * The application-level singleton is created by:
 *
 *     @/core/api/factory.ts
 *
 * This keeps transport implementation separate from application composition.
 */
export class ApiClient {
  private readonly client: AxiosInstance;

  private runtime:
    ApiRuntimeDependencies;

  private authentication:
    | ApiAuthenticationDependencies
    | undefined;

  private responseInterceptorId:
    | number
    | null = null;

  public constructor(
    config: ApiClientConfig,
    runtime:
      Partial<ApiRuntimeDependencies> = {},
    authentication?:
      ApiAuthenticationDependencies,
  ) {
    this.runtime = {
      tokenProvider:
        runtime.tokenProvider ??
        EMPTY_TOKEN_PROVIDER,

      tenantProvider:
        runtime.tenantProvider ??
        EMPTY_TENANT_PROVIDER,

      requestIdProvider:
        runtime.requestIdProvider ??
        DEFAULT_REQUEST_ID_PROVIDER,
    };

    this.authentication =
      authentication;

    this.client =
      axios.create({
        baseURL:
          this.buildBaseURL(config),

        timeout:
          config.timeout,

        withCredentials:
          config.withCredentials,
      });

    this.configureInterceptors();
  }

  /* ===========================================================================
   * Runtime Configuration
   * ===========================================================================
   */

  /**
   * Update runtime dependencies.
   *
   * Existing dependencies are preserved when only a subset is supplied.
   */
  public setRuntime(
    runtime:
      Partial<ApiRuntimeDependencies>,
  ): void {
    this.runtime = {
      ...this.runtime,
      ...runtime,
    };

    this.reinstallInterceptors();
  }

  /**
   * Replace the token provider.
   */
  public setTokenProvider(
    provider:
      ApiRuntimeDependencies[
        "tokenProvider"
      ],
  ): void {
    this.runtime = {
      ...this.runtime,
      tokenProvider:
        provider,
    };

    this.reinstallInterceptors();
  }

  /**
   * Replace the tenant provider.
   */
  public setTenantProvider(
    provider:
      ApiRuntimeDependencies[
        "tenantProvider"
      ],
  ): void {
    this.runtime = {
      ...this.runtime,
      tenantProvider:
        provider,
    };

    this.reinstallInterceptors();
  }

  /**
   * Replace the request-ID provider.
   */
  public setRequestIdProvider(
    provider:
      ApiRuntimeDependencies[
        "requestIdProvider"
      ],
  ): void {
    this.runtime = {
      ...this.runtime,
      requestIdProvider:
        provider,
    };

    this.reinstallInterceptors();
  }

  /**
   * Configure authentication response handling.
   */
  public setAuthenticationDependencies(
    dependencies:
      | ApiAuthenticationDependencies
      | undefined,
  ): void {
    this.authentication =
      dependencies;

    this.reinstallInterceptors();
  }

  /**
   * Expose the underlying Axios instance for infrastructure-level use.
   *
   * Feature modules should use ApiClient methods instead.
   */
  public get axios(): AxiosInstance {
    return this.client;
  }

  /* ===========================================================================
   * GET
   * ===========================================================================
   */

  public async get<T>(
    url: string,
    config?: ApiRequestConfig,
  ): Promise<ApiSuccessResponse<T>> {
    try {
      const response =
        await this.client.get<
          ApiResponse<T>
        >(
          url,
          config,
        );

      return this.unwrapResponse(
        response,
      );
    } catch (error) {
      throw this.handleError(
        error,
      );
    }
  }

  /* ===========================================================================
   * POST
   * ===========================================================================
   */

  public async post<
    T,
    TBody = unknown,
  >(
    url: string,
    data?: TBody,
    config?: ApiRequestConfig,
  ): Promise<ApiSuccessResponse<T>> {
    try {
      const response =
        await this.client.post<
          ApiResponse<T>
        >(
          url,
          data,
          config,
        );

      return this.unwrapResponse(
        response,
      );
    } catch (error) {
      throw this.handleError(
        error,
      );
    }
  }

  /* ===========================================================================
   * PUT
   * ===========================================================================
   */

  public async put<
    T,
    TBody = unknown,
  >(
    url: string,
    data?: TBody,
    config?: ApiRequestConfig,
  ): Promise<ApiSuccessResponse<T>> {
    try {
      const response =
        await this.client.put<
          ApiResponse<T>
        >(
          url,
          data,
          config,
        );

      return this.unwrapResponse(
        response,
      );
    } catch (error) {
      throw this.handleError(
        error,
      );
    }
  }

  /* ===========================================================================
   * PATCH
   * ===========================================================================
   */

  public async patch<
    T,
    TBody = unknown,
  >(
    url: string,
    data?: TBody,
    config?: ApiRequestConfig,
  ): Promise<ApiSuccessResponse<T>> {
    try {
      const response =
        await this.client.patch<
          ApiResponse<T>
        >(
          url,
          data,
          config,
        );

      return this.unwrapResponse(
        response,
      );
    } catch (error) {
      throw this.handleError(
        error,
      );
    }
  }

  /* ===========================================================================
   * DELETE
   * ===========================================================================
   */

  public async delete<T = null>(
    url: string,
    config?: ApiRequestConfig,
  ): Promise<ApiSuccessResponse<T>> {
    try {
      const response =
        await this.client.delete<
          ApiResponse<T>
        >(
          url,
          config,
        );

      return this.unwrapResponse(
        response,
      );
    } catch (error) {
      throw this.handleError(
        error,
      );
    }
  }

  /* ===========================================================================
   * Generic Request
   * ===========================================================================
   */

  public async request<T>(
    config: ApiRequestConfig,
  ): Promise<ApiSuccessResponse<T>> {
    try {
      const response =
        await this.client.request<
          ApiResponse<T>
        >(
          config,
        );

      return this.unwrapResponse(
        response,
      );
    } catch (error) {
      throw this.handleError(
        error,
      );
    }
  }

  /* ===========================================================================
   * Interceptors
   * ===========================================================================
   */

  private configureInterceptors(): void {
    this.client.interceptors.request.use(
      createRequestInterceptor(
        this.runtime,
      ),
    );

    this.responseInterceptorId =
      installResponseInterceptors(
        this.client,
        this.authentication ?? {},
      );
  }

  private reinstallInterceptors(): void {
    this.client.interceptors.request.clear();

    this.client.interceptors.response.clear();

    this.responseInterceptorId =
      null;

    this.configureInterceptors();
  }

  /* ===========================================================================
   * URL Configuration
   * ===========================================================================
   */

  /**
   * Build the Axios base URL from the canonical API configuration.
   *
   * Example:
   *
   *     baseURL = http://127.0.0.1:8000/api
   *     version = ""
   *
   * Result:
   *
   *     http://127.0.0.1:8000/api
   *
   * If version is configured:
   *
   *     baseURL = http://127.0.0.1:8000/api
   *     version = v1
   *
   * Result:
   *
   *     http://127.0.0.1:8000/api/v1
   */
  private buildBaseURL(
    config: ApiClientConfig,
  ): string {
    const baseURL =
      config.baseURL.replace(
        /\/+$/,
        "",
      );

    const version =
      config.version.replace(
        /^\/+|\/+$/g,
        "",
      );

    if (!version) {
      return baseURL;
    }

    return `${baseURL}/${version}`;
  }

  /* ===========================================================================
   * Error Handling
   * ===========================================================================
   */

  private handleError(
    error: unknown,
  ): ApiClientError {
    if (
      error instanceof
      ApiClientError
    ) {
      return error;
    }

    if (
      axios.isAxiosError(error)
    ) {
      return this.normalizeError(
        error,
      );
    }

    return new ApiClientError(
      {
        code:
          "UNKNOWN_ERROR",
        message:
          error instanceof Error
            ? error.message
            : "An unexpected error occurred.",
        details: null,
      },
      {
        statusCode: 0,
      },
    );
  }

  /* ===========================================================================
   * Response Contract
   * ===========================================================================
   */

  private unwrapResponse<T>(
    response: AxiosResponse<
      ApiResponse<T>
    >,
  ): ApiSuccessResponse<T> {
    const payload =
      response.data;

    if (
      !this.isApiEnvelope<T>(
        payload,
      )
    ) {
      throw new ApiClientError(
        {
          code:
            "INVALID_API_RESPONSE",
          message:
            "The server returned an invalid API response.",
          details:
            this.toJsonValue(
              payload,
            ),
        },
        {
          statusCode:
            response.status,
          response,
        },
      );
    }

    if (
      payload.success === false
    ) {
      throw this.createBackendError(
        payload,
        response,
      );
    }

    return payload;
  }

  private isApiEnvelope<T>(
    value: unknown,
  ): value is ApiResponse<T> {
    if (
      value === null ||
      typeof value !== "object"
    ) {
      return false;
    }

    return (
      "success" in value &&
      typeof (
        value as {
          success?: unknown;
        }
      ).success === "boolean"
    );
  }

  private createBackendError(
    payload: ApiErrorResponse,
    response: AxiosResponse,
  ): ApiClientError {
    return new ApiClientError(
      payload.error,
      {
        statusCode:
          response.status,
        meta:
          payload.meta,
        response,
      },
    );
  }

  /* ===========================================================================
   * Error Normalization
   * ===========================================================================
   */

  public normalizeError(
    error: AxiosError,
  ): ApiClientError {
    if (error.response) {
      return this.normalizeResponseError(
        error,
      );
    }

    if (
      error.code ===
      AxiosError.ERR_CANCELED
    ) {
      return new ApiClientError(
        {
          code:
            "REQUEST_CANCELLED",
          message:
            "The request was cancelled.",
          details: null,
        },
        {
          statusCode: 0,
        },
      );
    }

    if (
      error.code ===
        AxiosError.ETIMEDOUT ||
      error.code ===
        "ECONNABORTED"
    ) {
      return new ApiClientError(
        {
          code:
            "REQUEST_TIMEOUT",
          message:
            "The request timed out.",
          details: null,
        },
        {
          statusCode: 0,
        },
      );
    }

    return new ApiClientError(
      {
        code:
          "NETWORK_ERROR",
        message:
          "Unable to communicate with the server.",
        details: null,
      },
      {
        statusCode: 0,
      },
    );
  }

  private normalizeResponseError(
    error: AxiosError,
  ): ApiClientError {
    const response =
      error.response;

    if (!response) {
      return new ApiClientError(
        {
          code:
            "NETWORK_ERROR",
          message:
            "Unable to communicate with the server.",
          details: null,
        },
        {
          statusCode: 0,
        },
      );
    }

    const payload =
      response.data;

    if (
      this.isErrorResponse(
        payload,
      )
    ) {
      return this.createBackendError(
        payload,
        response,
      );
    }

    return new ApiClientError(
      {
        code:
          this.getStatusCode(
            response.status,
          ),
        message:
          this.getFallbackMessage(
            response.status,
          ),
        details:
          this.toJsonValue(
            payload,
          ),
      },
      {
        statusCode:
          response.status,
        meta:
          this.extractMeta(
            payload,
          ),
        response,
      },
    );
  }

  private isErrorResponse(
    value: unknown,
  ): value is ApiErrorResponse {
    if (
      value === null ||
      typeof value !== "object"
    ) {
      return false;
    }

    const candidate =
      value as {
        success?: unknown;
        error?: unknown;
      };

    return (
      candidate.success === false &&
      typeof candidate.error ===
        "object" &&
      candidate.error !== null
    );
  }

  private extractMeta(
    value: unknown,
  ): ApiMeta | null {
    if (
      value === null ||
      typeof value !== "object"
    ) {
      return null;
    }

    if (!("meta" in value)) {
      return null;
    }

    const meta =
      (
        value as {
          meta?: unknown;
        }
      ).meta;

    if (
      meta === null ||
      typeof meta !== "object"
    ) {
      return null;
    }

    return meta as ApiMeta;
  }

  private getStatusCode(
    statusCode?: number,
  ): string {
    switch (statusCode) {
      case 400:
        return "BAD_REQUEST";

      case 401:
        return "UNAUTHENTICATED";

      case 403:
        return "FORBIDDEN";

      case 404:
        return "RESOURCE_NOT_FOUND";

      case 405:
        return "OPERATION_NOT_ALLOWED";

      case 409:
        return "RESOURCE_CONFLICT";

      case 415:
        return "UNSUPPORTED_MEDIA_TYPE";

      case 429:
        return "RATE_LIMIT_EXCEEDED";

      case 500:
      case 501:
      case 502:
      case 503:
      case 504:
        return "INTERNAL_SERVER_ERROR";

      default:
        return "API_ERROR";
    }
  }

  private getFallbackMessage(
    statusCode?: number,
  ): string {
    switch (statusCode) {
      case 400:
        return "The request is invalid.";

      case 401:
        return "Authentication is required.";

      case 403:
        return "You do not have permission to perform this operation.";

      case 404:
        return "The requested resource was not found.";

      case 405:
        return "The requested method is not allowed.";

      case 409:
        return "The requested operation conflicts with existing data.";

      case 415:
        return "The submitted content type is not supported.";

      case 429:
        return "Too many requests. Please try again later.";

      case 500:
      case 501:
      case 502:
      case 503:
      case 504:
        return "An unexpected server error occurred.";

      default:
        return "The request failed.";
    }
  }

  /* ===========================================================================
   * JSON Conversion
   * ===========================================================================
   */

  private toJsonValue(
    value: unknown,
  ): JsonValue {
    if (value === null) {
      return null;
    }

    if (
      typeof value === "string" ||
      typeof value === "number" ||
      typeof value === "boolean"
    ) {
      return value;
    }

    if (Array.isArray(value)) {
      return value.map(
        (item) =>
          this.toJsonValue(item),
      );
    }

    if (
      typeof value === "object"
    ) {
      const result: {
        [key: string]: JsonValue;
      } = {};

      for (const [
        key,
        item,
      ] of Object.entries(
        value as Record<
          string,
          unknown
        >,
      )) {
        result[key] =
          this.toJsonValue(item);
      }

      return result;
    }

    return String(value);
  }
}

/* =============================================================================
 * Factory
 * =============================================================================
 */

/**
 * Create a DatavionOS API client.
 *
 * Application-level singleton creation belongs to:
 *
 *     src/core/api/factory.ts
 */
export function createApiClient(
  config: ApiClientConfig,
  runtime?:
    Partial<ApiRuntimeDependencies>,
  authentication?:
    ApiAuthenticationDependencies,
): ApiClient {
  return new ApiClient(
    config,
    runtime,
    authentication,
  );
}
